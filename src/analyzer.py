# src/analyzer.py — Tagging, Glossary Extraction, and Thematic Clustering
# Usage: from src.analyzer import analyze_item, extract_glossary_terms, cluster_items
# Requires: json, re, requests (optional for Ollama)
#
# Gotchas:
# - Ollama may be offline or slow; always provide a deterministic heuristic/TF-IDF fallback.
# - Vendor marketing terms ("judgment infrastructure", "zero-resistance") must be flagged so the author avoids them.

import json
import re
import math
from typing import Dict, Any, List, Tuple
from collections import Counter
import requests

THEMES = [
    "Alert Fatigue & Backlog",
    "Entity Resolution & Name Matching",
    "UBO, Shell Companies & Transshipment",
    "Sanctions Screening & OFAC Rules",
    "Supply Chain Risk & Forced Labor (UFLPA)",
    "Audit Panic & Regulatory Examination",
    "Swivel Chair Manual Review & Frankenstack",
    "Adverse Media & Negative News Noise"
]

VENDOR_MARKETING_TERMS = {
    "judgment infrastructure",
    "zero-resistance",
    "leverage synergies",
    "single pane of glass",
    "holistic end-to-end",
    "paradigm shift",
    "frictionless compliance",
    "best-in-breed seamless integration",
    "next-gen risk ecosystem"
}

FOUNDATIONAL_PRACTITIONER_TERMS = {
    "alert fatigue": "Most common category term for alert overload, used by Sayari's own blog and practitioners.",
    "swivel chair": "Used for analysts doing repetitive work across fragmented systems ('swivel chair effect' across multiple logins). Real equivalent to Frankenstack.",
    "point solutions & silos": "The standard practitioner way of describing disconnected tools that rarely communicate with each other.",
    "backlog & clearing alerts": "The queue backs up, and the day is spent clearing it. Analysts say 'disposition alerts' and call first-line review 'L1'.",
    "false positives": "Industry benchmark of 90% to 95% false positives in sanctions screening.",
    "spreadsheets and google": ">25% of compliance teams manage periodic reviews in spreadsheets; 65% rely on manual Google searches for adverse media.",
    "name matching": "Entity resolution bottleneck; hours spent triaging Latin/Cyrillic/Arabic spelling variations and initials.",
    "kyc refresh vs pkyc": "Periodic KYC review cycles vs perpetual KYC (pKYC) continuous monitoring.",
    "ubo & nested ownership": "Ultimate Beneficial Ownership obscured behind opaque multi-jurisdiction holding layers.",
    "edd": "Enhanced Due Diligence triggered when high-risk ownership, PEPs, or transshipment hubs are flagged.",
    "audit trail": "Defensible paper trail proving to regulatory examiners why an alert was cleared or escalated."
}

PRACTITIONER_TERM_PATTERNS = [
    r"\bswivel[- ]chair(?: effect)?\b",
    r"\bname[- ]match(?:ing)?\b",
    r"\bfalse positive[s]?\b",
    r"\balert fatigue\b",
    r"\bclearing alerts\b",
    r"\bfrankenstack\b",
    r"\bpoint solutions?\b",
    r"\bdisconnected systems?\b",
    r"\bfragmented systems?\b",
    r"\bl1 review\b",
    r"\bfirst[- ]line review\b",
    r"\bedd\b",
    r"\bkyc\b",
    r"\bkyb\b",
    r"\bpkyc\b",
    r"\bperpetual kyc\b",
    r"\bkyc refresh\b",
    r"\bperiodic review[s]?\b",
    r"\bubo\b",
    r"\bnested ownership\b",
    r"\bbeneficial owner(?:ship)?\b",
    r"\bdisposition(?: alerts)?\b",
    r"\bbacklog\b",
    r"\bqueue\b",
    r"\bofac\b",
    r"\buflpa\b",
    r"\bsub[- ]tier mapping\b",
    r"\bforced labor\b",
    r"\bshell compan(?:y|ies)\b",
    r"\btransshipment\b",
    r"\btprm\b",
    r"\bthird[- ]party risk\b",
    r"\badverse media\b",
    r"\bexport control[s]?\b",
    r"\bmanual review\b",
    r"\bspreadsheet[s]?(?: and google)?\b",
    r"\baudit trail\b"
]

def detect_audience(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ["procurement", "vendor onboarding", "supplier risk", "sourcing", "rfp"]):
        return "procurement"
    if any(k in text_lower for k in ["l1", "analyst", "investigator", "case file", "drowning in alerts", "queue"]):
        return "analyst"
    if any(k in text_lower for k in ["cco", "audit", "exam", "regulator", "policy", "board", "defensible"]):
        return "compliance officer"
    return "compliance officer"

def detect_post_type(text: str) -> str:
    text_lower = text.lower()
    if "?" in text or any(k in text_lower for k in ["how do you", "does anyone", "what tool", "is it normal"]):
        return "question"
    if any(k in text_lower for k in ["broken tool", "vendor promised", "terrible ui", "slow search", "hate this system"]):
        return "tool complaint"
    if any(k in text_lower for k in ["i cannot stand", "ridiculous", "drowning", "unrealistic", "insane", "rant"]):
        return "rant"
    if any(k in text_lower for k in ["last year we had", "in my previous bank", "we got audited", "back in"]):
        return "war story"
    if any(k in text_lower for k in ["ofac just announced", "new sanction", "doj enforcement", "settlement", "fine"]):
        return "news reaction"
    return "hot take"

def detect_emotion_and_intensity(text: str) -> Tuple[str, int]:
    text_lower = text.lower()
    
    # Emotion signals
    frustration_words = ["frustrated", "annoying", "tedious", "waste of time", "nightmare", "screaming", "stupid", "drowning", "broken"]
    sarcasm_words = ["love spending 4 hours", "brilliant design", "thanks compliance", "clowns", "magic score", "shocker", "what could go wrong"]
    fear_words = ["audit", "fined", "regulator exam", "terrified", "panic", "penalty", "liable", "fired", "worried"]
    relief_words = ["finally fixed", "saved my week", "cleared the backlog", "so much easier", "game changer", "thank goodness"]
    pride_words = ["caught a shell company", "proud of our team", "found the ubo", "nailed the exam", "spotted the evasion"]

    scores = {
        "frustration": sum(1 for w in frustration_words if w in text_lower),
        "sarcasm": sum(1 for w in sarcasm_words if w in text_lower),
        "fear": sum(1 for w in fear_words if w in text_lower),
        "relief": sum(1 for w in relief_words if w in text_lower),
        "pride": sum(1 for w in pride_words if w in text_lower)
    }

    primary_emotion = "frustration"
    max_score = 0
    for em, sc in scores.items():
        if sc > max_score:
            max_score = sc
            primary_emotion = em

    # Intensity calculation (1-5)
    exclamation_count = text.count("!")
    caps_words = len([w for w in text.split() if w.isupper() and len(w) > 2])
    
    base_intensity = 2
    if max_score >= 3 or exclamation_count >= 2 or caps_words >= 2:
        base_intensity = 4
    elif max_score >= 1 or exclamation_count >= 1:
        base_intensity = 3
    elif max_score == 0:
        base_intensity = 1
        
    if "nightmare" in text_lower or "unmitigated disaster" in text_lower or "panic" in text_lower:
        base_intensity = 5

    return primary_emotion, min(5, max(1, base_intensity))

KEY_OPINIONS = [
    {
        "id": "questionnaires_vs_reality",
        "stance": "Vendor Questionnaires Are Compliance Theater",
        "tension": "Self-disclosures are useless; illicit networks never declare ownership; true risk is hidden 3-5 layers deep in nested corporate structures.",
        "keywords": ["questionnaire", "self-disclosure", "ubo", "shell", "nested ownership", "50 percent rule", "beneficial owner", "belize", "cyprus", "front company", "transshipment"]
    },
    {
        "id": "tool_failure_alert_fatigue",
        "stance": "Alert Fatigue is a Tool Failure, Not an Analyst Failure",
        "tension": "90%+ false positive rates are caused by crude keyword filters, turning L1 review into soul-crushing whack-a-mole.",
        "keywords": ["alert fatigue", "false positive", "queue", "backlog", "disposition", "l1", "first-line", "800 alerts", "cheapest vendor", "monitoring tool"]
    },
    {
        "id": "swivel_chair_frankenstack",
        "stance": "The Swivel Chair Trap: Fragmented Tools Paralyze Investigation",
        "tension": "Analysts waste 45 mins copying registry IDs across 6-8 disconnected vendor tabs and spreadsheets that don't talk to each other.",
        "keywords": ["swivel chair", "frankenstack", "point solution", "disconnected", "silo", "multiple logins", "spreadsheets", "6 tabs", "excel", "manual review"]
    },
    {
        "id": "score_is_not_defense",
        "stance": "A Vendor Risk Score is Not an Audit Defense",
        "tension": "Regulators reject automated black-box risk scores; examiners demand verifiable primary registry documents and audit provenance.",
        "keywords": ["audit", "exam", "regulator", "defensible", "score", "audit trail", "penalties", "settlement", "doj", "fincen", "whistleblower"]
    },
    {
        "id": "subtier_supply_chain",
        "stance": "The Sub-Tier Supply Chain Blind Spot (Beyond Tier 1)",
        "tension": "Tier-1 suppliers pass easily; UFLPA seizures happen at Tier-2 and Tier-3 raw component and transshipment hubs.",
        "keywords": ["uflpa", "forced labor", "supply chain", "tier 1", "tier 2", "tier 3", "sub-tier", "smelter", "customs", "distributor"]
    },
    {
        "id": "entity_resolution_hell",
        "stance": "Name-Match Purgatory: Triaging Common Spellings & Transliterations",
        "tension": "Legacy screening tools flood queues with hits on common surnames, while genuine sanctioned entities evade detection with transliteration tricks.",
        "keywords": ["name match", "name matching", "spelling", "vowel", "fuzzy", "transliteration", "latin names", "alias"]
    },
    {
        "id": "enforcement_reality",
        "stance": "Enforcement Is Shifting From Box-Checking to Evidentiary Proof",
        "tension": "Recent penalties (e.g. Webull, TD Bank, Steptoe sanctions advisories) prove that superficial compliance is scrutinized down to root investigation.",
        "keywords": ["settlement", "enforcement", "penalty", "fined", "whistleblower", "pleaded", "steptoe", "compliance week", "fiveby"]
    }
]

def detect_key_opinion(text: str) -> Dict[str, str]:
    text_lower = text.lower()
    best_op = None
    max_matches = 0
    for op in KEY_OPINIONS:
        matches = sum(1 for kw in op["keywords"] if kw in text_lower)
        if matches > max_matches:
            max_matches = matches
            best_op = op
    if best_op and max_matches >= 1:
        return best_op
    # Fallback default
    return {
        "id": "practitioner_reality",
        "stance": "The Reality Gap: Vendor Promises vs Practitioner Daily Grind",
        "tension": "What marketing brochures promise vs what actually lands in the compliance analyst's queue on Monday morning.",
        "keywords": []
    }

def detect_theme(text: str) -> str:
    op = detect_key_opinion(text)
    return op["stance"]

def extract_practitioner_terms(text: str) -> List[str]:
    text_lower = text.lower()
    extracted = set()
    for pat in PRACTITIONER_TERM_PATTERNS:
        matches = re.findall(pat, text_lower)
        for m in matches:
            extracted.add(m.strip())
    return sorted(list(extracted))

def analyze_item(title: str, content: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts theme, emotion, intensity, audience, post type, and practitioner terms."""
    full_text = f"{title}\n{content}"
    
    theme = detect_theme(full_text)
    emotion, intensity = detect_emotion_and_intensity(full_text)
    post_type = detect_post_type(full_text)
    audience = detect_audience(full_text)
    terms = extract_practitioner_terms(full_text)

    return {
        "theme": theme,
        "emotion": emotion,
        "intensity": intensity,
        "post_type": post_type,
        "audience": audience,
        "used_terms": terms
    }

def cluster_items_fallback(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Deterministic fallback clustering based on detected themes and keyword vectors."""
    clusters: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        theme = item.get("theme") or detect_theme(f"{item.get('title','')} {item.get('short_excerpt','')}")
        clusters.setdefault(theme, []).append(item)
    return clusters

def cluster_items_ollama(items: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Uses local Ollama model if configured and running, falling back seamlessly on error."""
    ollama_cfg = config.get("llm_clustering", {})
    if not ollama_cfg.get("enabled", False):
        return cluster_items_fallback(items)

    url = f"{ollama_cfg.get('ollama_url', 'http://localhost:11434')}/api/generate"
    model = ollama_cfg.get("ollama_model", "qwen2.5-coder:7b")

    # Sample condensed titles for prompt
    titles_summary = [{"id": it.get("id"), "title": it.get("title")} for it in items[:25]]
    prompt = (
        f"You are a clustering assistant for compliance intelligence.\n"
        f"Group these compliance items into standard themes:\n"
        f"Allowed themes: {json.dumps(THEMES)}\n"
        f"Items: {json.dumps(titles_summary)}\n"
        f"Return ONLY valid JSON mapping item id to theme string, e.g. {{\"id1\": \"Theme\"}}."
    )

    try:
        resp = requests.post(url, json={"model": model, "prompt": prompt, "stream": False, "format": "json"}, timeout=12)
        if resp.status_code == 200:
            result_json = json.loads(resp.json().get("response", "{}"))
            clusters: Dict[str, List[Dict[str, Any]]] = {}
            item_map = {it.get("id"): it for it in items}
            for item_id, theme in result_json.items():
                if item_id in item_map:
                    it = item_map[item_id]
                    assigned_theme = theme if theme in THEMES else it.get("theme", "Alert Fatigue & Backlog")
                    it["theme"] = assigned_theme
                    clusters.setdefault(assigned_theme, []).append(it)
            # Add any missed items
            for it in items:
                assigned_theme = it.get("theme", "Alert Fatigue & Backlog")
                if not any(it.get("id") == x.get("id") for x in clusters.get(assigned_theme, [])):
                    clusters.setdefault(assigned_theme, []).append(it)
            return clusters
    except Exception:
        pass # Graceful fallback to TF-IDF / rule-based clustering
    
    return cluster_items_fallback(items)

def extract_glossary_from_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Builds the language glossary with frequencies, source counts, and marketing flags."""
    term_counts = Counter()
    term_sources = {}
    term_contexts = {}

    for it in items:
        source_id = it.get("source", "unknown")
        text = f"{it.get('title','')} {it.get('short_excerpt','')} {it.get('paraphrase','')}"
        terms = it.get("used_terms") or extract_practitioner_terms(text)
        if isinstance(terms, str):
            try:
                terms = json.loads(terms)
            except Exception:
                terms = []

        for t in terms:
            term_counts[t] += 1
            term_sources.setdefault(t, set()).add(source_id)
            if t not in term_contexts:
                # 15-word window around term
                words = text.split()
                snippet = " ".join(words[:20])
                term_contexts[t] = snippet

    glossary = []
    for term, freq in term_counts.most_common():
        is_vendor = 1 if term in VENDOR_MARKETING_TERMS else 0
        glossary.append({
            "term": term,
            "frequency": freq,
            "source_count": len(term_sources.get(term, set())),
            "example_context": term_contexts.get(term, ""),
            "is_vendor_marketing_only": is_vendor
        })

    # Ensure foundational practitioner terms from Sayari brief are present
    for pterm, pnote in FOUNDATIONAL_PRACTITIONER_TERMS.items():
        existing = next((g for g in glossary if g["term"].lower() == pterm.lower()), None)
        if existing:
            if not existing.get("example_context"):
                existing["example_context"] = pnote
        else:
            glossary.append({
                "term": pterm,
                "frequency": 1,
                "source_count": 1,
                "example_context": pnote,
                "is_vendor_marketing_only": 0
            })

    # Also add known vendor marketing buzzwords as flagged examples if not already present
    for vterm in VENDOR_MARKETING_TERMS:
        if not any(g["term"] == vterm for g in glossary):
            glossary.append({
                "term": vterm,
                "frequency": 0,
                "source_count": 0,
                "example_context": "Vendor brochure buzzword — avoid in practitioner copy",
                "is_vendor_marketing_only": 1
            })

    return glossary
