# tests/test_filters.py — Unit tests for compliance filtering rules
# Usage: pytest tests/test_filters.py

import pytest
from src.filters import evaluate_item

@pytest.fixture
def sample_config():
    return {
        "keywords": {
            "seed_keywords": [
                "alert fatigue",
                "false positive",
                "name matching",
                "sanctions screening",
                "kyc",
                "kyb",
                "ubo",
                "swivel chair",
                "backlog",
                "frankenstack",
                "manual review"
            ]
        },
        "filter_rules": {
            "drop_patterns": [
                "cams exam",
                "study guide",
                "resume review",
                "promo code"
            ],
            "frustration_exception_words": [
                "swivel chair",
                "backlog",
                "nightmare",
                "frustration",
                "drowning"
            ]
        }
    }

def test_irrelevant_post_dropped(sample_config):
    title = "Best dinner recipes for Friday"
    body = "Looking for easy pasta recipes with garlic and olive oil."
    passed, reason, matched = evaluate_item(title, body, sample_config)
    assert passed is False
    assert "No compliance seed keywords matched" in reason

def test_relevant_kyc_post_passed(sample_config):
    title = "Stuck in name matching hell"
    body = "Our KYC analyst queue is overflowing because of false positives on common Latin names."
    passed, reason, matched = evaluate_item(title, body, sample_config)
    assert passed is True
    assert "name matching" in matched
    assert "kyc" in matched

def test_career_exam_post_dropped(sample_config):
    title = "Passed my CAMS exam today! Tips for KYC job search"
    body = "Used the official study guide for 3 months and passed with 95. Ready to break into KYC."
    passed, reason, matched = evaluate_item(title, body, sample_config)
    assert passed is False
    assert "Dropped: career/exam-prep" in reason

def test_career_exam_post_with_daily_frustration_passed(sample_config):
    title = "Passed CAMS exam, but real L1 review is a nightmare"
    body = "The CAMS exam never warned me about this backlog and swivel chair manual review across 6 tabs."
    passed, reason, matched = evaluate_item(title, body, sample_config)
    assert passed is True
    assert "swivel chair" in matched
    assert "manual review" in matched

def test_no_false_positive_acronym_substring_match(sample_config):
    # 'ubo' shouldn't match 'suborbital'
    title = "Space travel and suborbital flights"
    body = "Discussion on rocket telemetry."
    passed, reason, matched = evaluate_item(title, body, sample_config)
    assert passed is False
    assert matched == []

def test_vendor_promo_post_dropped(sample_config):
    # Vendor trying to sell a tool in the subreddit
    sample_config["filter_rules"]["drop_patterns"].extend(["we built a tool", "schedule a demo", "free trial"])
    title = "We built a tool to automate sanctions screening"
    body = "Tired of manual review? Check out our tool and schedule a demo for a free trial."
    passed, reason, matched = evaluate_item(title, body, sample_config)
    assert passed is False
    assert "Dropped: career/exam-prep" in reason or "Dropped" in reason

def test_practitioner_comment_on_ad_passed(sample_config):
    # An analyst roasting or questioning a vendor promo thread
    sample_config["filter_rules"]["drop_patterns"].extend(["we built a tool", "schedule a demo", "free trial"])
    title = "Practitioner reaction to vendor pitch ('We built a tool to automate sanctions screening...')"
    comment_body = "Another tool promising zero false positives? Does this actually handle fuzzy name matching or is our backlog still stuck with 90% manual review?"
    passed, reason, matched = evaluate_item(title, comment_body, sample_config)
    assert passed is True
    assert "false positive" in matched or "name matching" in matched or "backlog" in matched
