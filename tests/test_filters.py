# tests/test_filters.py — Unit tests for listener relevance filtering (filters v2)
# Usage: PYTHONPATH=. pytest tests/

import pytest
from src.filters import evaluate_item, source_lane


@pytest.fixture
def cfg():
    return {
        "keywords": {
            "specific_terms": ["false positive", "false positives", "name matching", "sanctions screening",
                               "kyc", "kyb", "ubo", "ofac", "frankenstack", "cost centre"],
            "generic_terms": ["compliance", "swivel chair", "backlog", "manual review", "audit", "screening"],
        },
        "source_tiers": {"core": ["AMLCompliance", "compliance"], "adjacent": ["business", "FinancialCareers"]},
        "filter_rules": {
            "drop_patterns": ["cams exam", "study guide", "resume review", "promo code", "salary", "i passed"],
            "frustration_exception_words": ["swivel chair", "backlog", "nightmare", "drowning"],
        },
    }


def test_irrelevant_post_dropped(cfg):
    passed, reason, _ = evaluate_item("Best dinner recipes", "Easy garlic pasta.", cfg)
    assert not passed and "No compliance seed keywords" in reason


def test_core_kyc_post_passed(cfg):
    passed, _, matched = evaluate_item("Stuck in name matching hell",
                                       "Our KYC queue is overflowing with false positives.", cfg,
                                       source="reddit:r/AMLCompliance:post:hot")
    assert passed and "name matching" in matched and "kyc" in matched


def test_offtopic_subreddit_dropped_even_with_keyword(cfg):
    # v1 bug: "swivel chair" for a nursing chair passed from r/deinfluencingPH
    passed, reason, _ = evaluate_item("Deinfluence me: swivel chair for first time mom", "nursing chair", cfg,
                                      source="reddit:r/r/deinfluencingPH:post")
    assert not passed and "Off-topic" in reason


def test_subreddit_name_is_not_a_keyword(cfg):
    # v1 bug: r/compliance auto-matched "compliance", so this passed
    passed, _, _ = evaluate_item("Practitioner reaction", "Thanks man", cfg, source="reddit:r/compliance:comment")
    assert not passed


def test_core_sub_generic_term_is_enough(cfg):
    passed, _, _ = evaluate_item("Third analyst gone in 4 months", "The backlog keeps growing.", cfg,
                                 source="reddit:r/AMLCompliance:post:targeted")
    assert passed


def test_edge_sub_single_generic_term_dropped(cfg):
    passed, reason, _ = evaluate_item("Career question", "Is compliance a good career?", cfg,
                                      source="reddit:r/FinancialCareers:comment:targeted")
    assert not passed and "Weak signal" in reason


def test_edge_sub_specific_term_passed(cfg):
    passed, _, _ = evaluate_item("Sanctions", "Are you manually looking up each entity on the OFAC website?", cfg,
                                 source="reddit:r/r/business:comment")
    assert passed


def test_rss_is_news_lane(cfg):
    assert source_lane("rss:Compliance Week", cfg) == "news"
    assert source_lane("reddit:r/r/AMLCompliance:comment", cfg) == "practitioner"
    assert source_lane("reddit:r/business:comment", cfg) == "edge"


def test_career_post_dropped_unless_frustration(cfg):
    passed, reason, _ = evaluate_item("I passed! KYC exam", "Used the study guide", cfg,
                                      source="reddit:r/AMLCompliance:post:hot")
    assert not passed and "career/exam-prep" in reason
    passed, _, _ = evaluate_item("Passed CAMS exam, but L1 is a nightmare",
                                 "Nobody warned me about this backlog and swivel chair manual review.", cfg,
                                 source="reddit:r/AMLCompliance:post:hot")
    assert passed


def test_no_acronym_substring_match(cfg):
    passed, _, matched = evaluate_item("Space travel and suborbital flights", "Rocket telemetry.", cfg)
    assert not passed and matched == []
