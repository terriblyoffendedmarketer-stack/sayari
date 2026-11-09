# src/filters.py — Relevance filter for listener items (v2, 2026-11-09)
# Usage: passed, reason, matched = evaluate_item(title, body, config, source="reddit:r/AMLCompliance:comment:hot")
#        lane = source_lane(source, config)   # "practitioner" | "edge" | "news" | "manual" | "offtopic"
# Requires: re, typing. Config keys: keywords.specific_terms, keywords.generic_terms,
#           source_tiers.core / source_tiers.adjacent, filter_rules.drop_patterns / frustration_exception_words.
#
# Rules:
#   - Reddit items from subs not in source_tiers are dropped (off-topic).
#   - Core subs (practitioner lane): need 1 specific term OR 1 generic term.
#   - Adjacent subs (edge lane) and RSS (news lane): need 1 specific term OR 2+ generic terms.
#   - Career / exam / promo patterns drop the item unless it also names a daily-work frustration.
#
# Gotchas:
# - v1 counted the subreddit NAME as a keyword (r/compliance -> "compliance"), so "Thanks man" passed. Never
#   add source text to the keyword haystack again.
# - v1 passed on ONE generic word from anywhere on Reddit: "swivel chair" (a nursing chair in r/deinfluencingPH),
#   "backlog" (recruiting in r/ModernHiring). Generic words only count inside core subs or in combination.
# - Sources look like "reddit:r/r/AMLCompliance:comment" (double r/) as well as "reddit:r/AMLCompliance:...";
#   _subreddit() handles both.
# - Word boundaries matter so "ubo" doesn't match "suborbital".

import re
from typing import Tuple, List, Dict, Any, Optional


def _terms(config: Dict[str, Any], key: str) -> List[str]:
    return [t.lower() for t in config.get("keywords", {}).get(key, []) or []]


def get_specific_terms(config: Dict[str, Any]) -> List[str]:
    # seed_keywords kept as a backward-compatible alias for specific terms
    return _terms(config, "specific_terms") + _terms(config, "seed_keywords")


def get_generic_terms(config: Dict[str, Any]) -> List[str]:
    return _terms(config, "generic_terms")


def get_drop_patterns(config: Dict[str, Any]) -> List[str]:
    return [dp.lower() for dp in config.get("filter_rules", {}).get("drop_patterns", [])]


def get_frustration_exceptions(config: Dict[str, Any]) -> List[str]:
    return [fe.lower() for fe in config.get("filter_rules", {}).get("frustration_exception_words", [])]


def find_matched_terms(text: str, term_list: List[str]) -> List[str]:
    """Finds which terms appear in the text using word boundaries (a trailing plural 's' is allowed)."""
    text_lower = text.lower()
    return [t for t in term_list if re.search(r'\b' + re.escape(t) + r's?\b', text_lower)]


def _subreddit(source: str) -> Optional[str]:
    m = re.match(r'reddit:(?:r/)+([^:]+)', source or "")
    return m.group(1).lower() if m else None


def source_lane(source: str, config: Dict[str, Any]) -> str:
    """Classifies where an item came from, which decides how strict the filter is and what it feeds."""
    s = (source or "").lower()
    if s.startswith("rss:"):
        return "news"
    if s.startswith("manual:"):
        return "manual"
    sub = _subreddit(source)
    if sub is None:
        return "practitioner" if not s else "news"
    tiers = config.get("source_tiers", {})
    core = {x.lower() for x in tiers.get("core", [])}
    adjacent = {x.lower() for x in tiers.get("adjacent", [])}
    if not core and not adjacent:
        return "practitioner"  # no tiers configured (e.g. unit tests): don't gate by source
    if sub in core:
        return "practitioner"
    if sub in adjacent:
        return "edge"
    return "offtopic"


def evaluate_item(title: str, text_content: str, config: Dict[str, Any], source: str = "") -> Tuple[bool, str, List[str]]:
    """Returns (passed, reason, matched_terms)."""
    combined_text = f"{title} {text_content}".strip()
    if not combined_text:
        return False, "Empty content", []

    lane = source_lane(source, config)
    if lane == "offtopic":
        return False, f"Off-topic subreddit (r/{_subreddit(source)} is not in source_tiers)", []

    specific = find_matched_terms(combined_text, get_specific_terms(config))
    generic = find_matched_terms(combined_text, get_generic_terms(config))
    matched = specific + [g for g in generic if g not in specific]

    if not matched:
        return False, "No compliance seed keywords matched", []
    if lane in ("edge", "news") and not specific and len(generic) < 2:
        return False, f"Weak signal for {lane} source: only generic term '{generic[0]}'", matched

    # Career / exam-prep / promo patterns. For comments on vendor posts, judge the comment body only.
    text_for_drop_check = text_content if "practitioner reaction to vendor" in title.lower() else combined_text
    matched_drops = find_matched_terms(text_for_drop_check, get_drop_patterns(config))
    if matched_drops and not find_matched_terms(combined_text, get_frustration_exceptions(config)):
        return False, f"Dropped: career/exam-prep pattern '{matched_drops[0]}' with no daily-work frustration", matched

    return True, "Passed", matched
