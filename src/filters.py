# src/filters.py — Keyword and relevance filtering engine
# Usage: item_passes, reason, matched_keywords = evaluate_item(title, body, config)
# Requires: re, typing
#
# Gotchas:
# - Don't drop career/exam posts if they mention actual daily-work frustrations (e.g. "swivel chair", "backlog").
# - Word boundaries are critical so short acronyms like "kyc" or "ubo" don't falsely match inside words (e.g. "skyscrapers").

import re
from typing import Tuple, List, Dict, Any

def get_keywords(config: Dict[str, Any]) -> List[str]:
    return [kw.lower() for kw in config.get("keywords", {}).get("seed_keywords", [])]

def get_drop_patterns(config: Dict[str, Any]) -> List[str]:
    return [dp.lower() for dp in config.get("filter_rules", {}).get("drop_patterns", [])]

def get_frustration_exceptions(config: Dict[str, Any]) -> List[str]:
    return [fe.lower() for fe in config.get("filter_rules", {}).get("frustration_exception_words", [])]

def find_matched_terms(text: str, term_list: List[str]) -> List[str]:
    """Finds which seed terms appear in the text using word boundaries."""
    text_lower = text.lower()
    matched = []
    for term in term_list:
        # Escape term and match with word boundary
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, text_lower):
            matched.append(term)
    return matched

def evaluate_item(title: str, text_content: str, config: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
    """
    Evaluates whether an item should be kept or dropped.
    Returns:
      (passed: bool, drop_reason: str, matched_keywords: List[str])
    """
    combined_text = f"{title} {text_content}".strip()
    if not combined_text:
        return False, "Empty content", []

    seed_keywords = get_keywords(config)
    drop_patterns = get_drop_patterns(config)
    frustration_exceptions = get_frustration_exceptions(config)

    matched_keywords = find_matched_terms(combined_text, seed_keywords)

    # Must match at least one relevant compliance keyword
    if not matched_keywords:
        return False, "No compliance seed keywords matched", []

    # Check for career / exam-prep / promo patterns
    matched_drops = find_matched_terms(combined_text, drop_patterns)
    if matched_drops:
        # Check if saved by a daily-work frustration exception
        matched_frustrations = find_matched_terms(combined_text, frustration_exceptions)
        if not matched_frustrations:
            return False, f"Dropped: career/exam-prep pattern '{matched_drops[0]}' with no daily-work frustration", matched_keywords

    return True, "Passed", matched_keywords
