# src/collectors/rss.py — RSS and Public Feed Collector
# Usage: from src.collectors.rss import collect_rss_feeds
# Requires: feedparser, requests, urllib.robotparser
#
# Hard rules:
# - Use only publicly available RSS headlines & summaries.
# - Never bypass paywalls or anti-bot measures.
# - If blocked or robots.txt disallows, log it to blocked_sources.
# - Excerpt clipped to max 25 words + paraphrased summary. No full articles.

import hashlib
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from typing import List, Dict, Any, Tuple
import feedparser
import requests

from src.db import clip_to_25_words, log_blocked_source

def check_robots_txt(feed_url: str, user_agent: str) -> bool:
    """Checks if fetching the RSS feed is permitted under robots.txt."""
    try:
        parsed = urlparse(feed_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        # Fetch robots.txt with low timeout
        resp = requests.get(robots_url, headers={"User-Agent": user_agent}, timeout=5)
        if resp.status_code == 200:
            rp.parse(resp.text.splitlines())
            return rp.can_fetch(user_agent, feed_url)
        return True # If no robots.txt exists, standard public web access is permitted
    except Exception:
        return True # Default to permissible if host has no reachable robots.txt

def collect_from_rss_source(source_info: Dict[str, Any], config: Dict[str, Any], db_conn) -> List[Dict[str, Any]]:
    name = source_info.get("name")
    url = source_info.get("url")
    user_agent = config.get("privacy_and_compliance", {}).get("user_agent", "SayariContentResearch/1.0")

    if not check_robots_txt(url, user_agent):
        print(f"[rss] robots.txt disallows access to {name} ({url}). Logging as blocked.")
        log_blocked_source(db_conn, name, url, "robots.txt disallowed access")
        return []

    items = []
    try:
        headers = {"User-Agent": user_agent}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 403 or resp.status_code == 401:
            print(f"[rss] HTTP {resp.status_code} on {name}. Logging as blocked.")
            log_blocked_source(db_conn, name, url, f"HTTP {resp.status_code} paywall or login requirement")
            return []
            
        if resp.status_code != 200:
            print(f"[rss] HTTP {resp.status_code} on {name}.")
            return []

        feed = feedparser.parse(resp.content)
        if feed.bozo and not feed.entries:
            print(f"[rss] Failed to parse feed for {name}.")
            return []

        for entry in feed.entries[:15]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            
            # Deterministic ID based on link/title
            raw_id = link or f"{name}:{title}"
            item_id = f"rss_{hashlib.md5(raw_id.encode('utf-8')).hexdigest()[:12]}"
            
            # Publication date
            published = entry.get("published", "") or entry.get("updated", "")
            date_str = published[:10] if len(published) >= 10 else time.strftime('%Y-%m-%d')

            short_excerpt = clip_to_25_words(f"{title}. {summary}")
            paraphrase = clip_to_25_words(summary) or title

            items.append({
                "id": item_id,
                "source": f"rss:{name}",
                "url": link,
                "date": date_str,
                "title": title,
                "short_excerpt": short_excerpt,
                "paraphrase": paraphrase,
                "upvotes": 0,
                "comment_count": 0,
                "paraphrased_top_comments": []
            })

    except requests.exceptions.RequestException as e:
        print(f"[rss error] Connection failed for {name}: {e}")
        log_blocked_source(db_conn, name, url, f"Network/Connection error: {str(e)[:80]}")
    except Exception as e:
        print(f"[rss error] Unexpected error for {name}: {e}")

    return items
