# src/collectors/apify.py — Apify Reddit Scraper Integration
# Usage: from src.collectors.apify import collect_apify_reddit
# Requires: requests, json, time

import os
import time
import requests
from typing import List, Dict, Any, Optional
from src.db import clip_to_25_words

ACTOR_ID = "mw5JvRF7kSxjfNqdu" # coding-doctor-omar/Reddit-Scraper-Pro

def determine_time_bucket(submitted_at: Optional[str]) -> str:
    """Classifies signal into foundational voice vs current regulatory reality."""
    if not submitted_at:
        return "current_regulatory"
    try:
        # submitted_at example: '2024-05-12T14:20:00.000Z'
        year = int(submitted_at[:4])
        current_year = 2026
        if current_year - year >= 2:
            return "foundational_voice" # Timeless mindset, complaints, coping mechanisms
        elif current_year - year >= 1:
            return "current_regulatory" # Modern post-2022 sanctions, UFLPA, CTA
        else:
            return "fresh_pulse" # Live chatter, breaking queue spikes
    except Exception:
        return "current_regulatory"

def run_apify_query(api_token: str, query: str, max_results: int = 15, include_comments: bool = True) -> List[Dict[str, Any]]:
    """Runs a query on Reddit-Scraper-Pro actor and retrieves dataset items."""
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "maxResults": max_results,
        "scrapingMode": "keywordSearch",
        "query": query,
        "includeComments": include_comments,
        "maxTopCommentsPerPost": 5
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code not in (200, 201):
            print(f"[apify] Failed to trigger run for '{query}': HTTP {resp.status_code}")
            return []

        run_data = resp.json().get("data", {})
        run_id = run_data.get("id")
        print(f"[apify] Launched run {run_id} for query '{query}'...")

        # Poll run completion
        for _ in range(15):
            time.sleep(3)
            status_resp = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}", headers=headers, timeout=10)
            if status_resp.status_code == 200:
                status = status_resp.json().get("data", {}).get("status")
                if status == "SUCCEEDED":
                    ds_id = status_resp.json().get("data", {}).get("defaultDatasetId")
                    items_resp = requests.get(f"https://api.apify.com/v2/datasets/{ds_id}/items", headers=headers, timeout=15)
                    if items_resp.status_code == 200:
                        return items_resp.json()
                    break
                elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                    print(f"[apify] Run {run_id} ended with status: {status}")
                    break

        return []
    except Exception as e:
        print(f"[apify] Error executing run: {e}")
        return []

def run_apify_community(api_token: str, subreddit_name: str, sort: str = "top-all-time", max_results: int = 12) -> List[Dict[str, Any]]:
    """Runs a targeted subreddit sweep on Reddit-Scraper-Pro with specific sort filter (top-all-time, top-past-year, hot)."""
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "maxResults": max_results,
        "scrapingMode": "standard",
        "sort": sort,
        "subredditUrls": [{"url": f"https://www.reddit.com/r/{subreddit_name}/"}],
        "includeComments": True,
        "maxTopCommentsPerPost": 5
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code not in (200, 201):
            print(f"[apify] Failed to trigger community run for r/{subreddit_name} ({sort}): HTTP {resp.status_code}")
            return []

        run_data = resp.json().get("data", {})
        run_id = run_data.get("id")
        print(f"[apify] Launched community run {run_id} for r/{subreddit_name} (sort: {sort})...")

        for _ in range(18):
            time.sleep(3)
            status_resp = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}", headers=headers, timeout=10)
            if status_resp.status_code == 200:
                status = status_resp.json().get("data", {}).get("status")
                if status == "SUCCEEDED":
                    ds_id = status_resp.json().get("data", {}).get("defaultDatasetId")
                    items_resp = requests.get(f"https://api.apify.com/v2/datasets/{ds_id}/items", headers=headers, timeout=15)
                    if items_resp.status_code == 200:
                        return items_resp.json()
                    break
                elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                    print(f"[apify] Run {run_id} ended with status: {status}")
                    break

        return []
    except Exception as e:
        print(f"[apify] Error executing community run: {e}")
        return []

def _load_env_token() -> str:
    token = os.environ.get("APIFY_TOKEN", "").strip()
    if token:
        return token
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("APIFY_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return ""

def collect_from_apify(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Sweeps high-priority Reddit signals using Apify:
    1. Targeted Subreddits (AMLCompliance, compliance, financialcrime) stratified by sort:
       - 'top-all-time': Foundational mindset and timeless rants (5-10 years ago)
       - 'top-past-year': High engagement from the last 12 months (modern regulatory landscape)
       - 'hot': Live practitioner chatter
    2. High-signal keyword queries for niche topics (false positives, swivel chair, shell companies)
    Extracts posts and unfiltered comments, tagging them by vintage (foundational vs current).
    """
    api_token = config.get("apify", {}).get("api_token", "").strip() or _load_env_token()

    collected = []
    seen_ids = set()

    def process_items(raw_items: List[Dict[str, Any]], default_sub: str, stream_tag: str):
        for item in raw_items:
            sub_id = item.get("submissionId") or item.get("parentId")
            if not sub_id or sub_id in seen_ids:
                continue
            seen_ids.add(sub_id)

            sub_type = item.get("submissionType", "post")
            subreddit = item.get("subreddit") or default_sub
            date_str = (item.get("submittedAt") or time.strftime("%Y-%m-%d"))[:10]
            time_bucket = determine_time_bucket(item.get("submittedAt"))
            url = item.get("submissionUrl") or item.get("parentPostUrl") or f"https://reddit.com/{sub_id}"

            if sub_type == "comment":
                # Real practitioner comment or objection
                body = item.get("bodyText") or ""
                if len(body) < 15 or body.lower().startswith("i am a bot"):
                    continue
                title = f"Practitioner reaction on r/{subreddit} ('{body[:60]}...')"
                short_excerpt = clip_to_25_words(body)
                paraphrase = body[:180] + ("..." if len(body) > 180 else "")
            else:
                # Top, Hot, or Foundational Post
                title = item.get("title") or "Reddit compliance post"
                body = item.get("bodyText") or ""
                short_excerpt = clip_to_25_words(f"{title}. {body}")
                paraphrase = f"{title}. {body}"[:180] + ("..." if len(f"{title}. {body}") > 180 else "")

            collected.append({
                "id": f"apify_{sub_id}",
                "source": f"reddit:r/{subreddit}:{sub_type}:{stream_tag}",
                "url": url,
                "date": date_str,
                "time_bucket": time_bucket,
                "title": title.strip(),
                "short_excerpt": short_excerpt,
                "paraphrase": paraphrase,
                "upvotes": int(item.get("score") or 0),
                "comment_count": int(item.get("numComments") or 0),
                "paraphrased_top_comments": []
            })

    # Strategy 1: Targeted Community Sort Sweeps (Top All-Time, Top Past Year, Hot)
    target_subs = ["AMLCompliance", "compliance", "financialcrime"]
    sort_plans = [
        ("top-all-time", 8, "top_all"),
        ("top-past-year", 10, "top_year"),
        ("hot", 8, "hot")
    ]

    for sub_name in target_subs:
        for sort_filter, limit, tag in sort_plans:
            print(f"[apify] Sweeping r/{sub_name} with sort='{sort_filter}' (limit={limit})...")
            items = run_apify_community(api_token, sub_name, sort=sort_filter, max_results=limit)
            print(f"        -> {len(items)} items received from r/{sub_name} ({tag}).")
            process_items(items, sub_name, tag)

    # Strategy 2: Niche Keyword Searches across Reddit
    search_queries = [
        "AML compliance false positives",
        "sanctions screening backlog",
        "beneficial ownership shell company"
    ]
    for q in search_queries:
        print(f"[apify] Sweeping signals for keyword: '{q}'...")
        items = run_apify_query(api_token, q, max_results=6, include_comments=True)
        print(f"        -> {len(items)} keyword items received.")
        process_items(items, "AMLCompliance", "keyword")

    return collected
