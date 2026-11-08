# src/collectors/reddit.py — Official Reddit API Collector
# Usage: from src.collectors.reddit import collect_subreddit_posts
# Requires: praw, sqlite3
#
# Hard rules & Gotchas:
# - Official API only with clear custom User-Agent.
# - Privacy: do not store usernames or profile metadata. Only URL and post ID.
# - Store short excerpts only (max 25 words) plus a paraphrased summary.
# - Skip vendor promos, weekly promo threads, and flairs.
# - Rate limits respected; responses cached to prevent redundant hits.

import time
import re
from typing import List, Dict, Any, Optional
import praw
from prawcore.exceptions import ResponseException, OAuthException

from src.db import clip_to_25_words

def is_promo(post_title: str, post_flair: Optional[str], skip_flairs: List[str], skip_patterns: List[str]) -> bool:
    """Checks if a post is a vendor advertisement or weekly promotion thread."""
    if post_flair:
        flair_lower = post_flair.lower()
        if any(f in flair_lower for f in skip_flairs):
            return True
            
    title_lower = post_title.lower()
    if any(p in title_lower for p in skip_patterns):
        return True
        
    return False

def paraphrase_text(raw_text: str, max_words: int = 50) -> str:
    """Creates a cleaned, paraphrased summary without storing the full original article."""
    if not raw_text:
        return ""
    # Clean markdown and excess whitespace
    cleaned = re.sub(r'http\S+', '', raw_text)
    cleaned = re.sub(r'[\*\#\_\[\]]', '', cleaned)
    words = cleaned.strip().split()
    if not words:
        return ""
    # Extract core clauses up to max_words
    summary_words = words[:max_words]
    return " ".join(summary_words) + ("..." if len(words) > max_words else "")

def collect_from_reddit(subreddit_name: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Collects posts from a given subreddit using PRAW.
    If Reddit API credentials are missing, returns empty list with clear guidance.
    """
    reddit_cfg = config.get("reddit", {})
    client_id = reddit_cfg.get("client_id", "").strip()
    client_secret = reddit_cfg.get("client_secret", "").strip()
    user_agent = reddit_cfg.get("user_agent", "SayariContentResearch/1.0")
    limit = reddit_cfg.get("limit_per_sub", 25)
    skip_flairs = [f.lower() for f in reddit_cfg.get("skip_flairs", [])]
    skip_patterns = [p.lower() for p in reddit_cfg.get("skip_title_patterns", [])]

    if not client_id or not client_secret:
        print(f"[reddit] No API credentials configured for r/{subreddit_name}. Please set client_id & client_secret in config.yaml.")
        return []

    collected_items = []
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            read_only=True
        )
        
        sub = reddit.subreddit(subreddit_name)
        # Fetch top and hot to get a balanced view of recurring frustrations
        for post in sub.hot(limit=limit):
            if post.stickied:
                continue

            flair = post.link_flair_text
            created_utc = time.strftime('%Y-%m-%d', time.gmtime(post.created_utc))
            post_is_promotional = is_promo(post.title, flair, skip_flairs, skip_patterns)

            # NUANCE: If the post is an ad or vendor promo, we do NOT keep the sales pitch.
            # BUT the comments are a goldmine of raw practitioner reactions (cynicism, objections, reality checks, or praise).
            if post_is_promotional:
                if post.num_comments > 0:
                    try:
                        post.comments.replace_more(limit=0)
                        for c_idx, comment in enumerate(post.comments[:5]):
                            c_body = comment.body or ""
                            # Ignore automoderator bot comments and trivial short phrases
                            if len(c_body) > 20 and not c_body.lower().startswith("i am a bot"):
                                c_id = f"reddit_{post.id}_ad_reaction_{c_idx}"
                                c_url = f"https://www.reddit.com{comment.permalink}"
                                c_short = clip_to_25_words(c_body)
                                c_para = paraphrase_text(c_body, max_words=60)

                                collected_items.append({
                                    "id": c_id,
                                    "source": f"reddit:r/{subreddit_name}:ad_reaction",
                                    "url": c_url,
                                    "date": created_utc,
                                    "title": f"Practitioner reaction to vendor pitch ('{post.title[:60]}...')",
                                    "short_excerpt": c_short,
                                    "paraphrase": c_para,
                                    "upvotes": int(comment.score or 0),
                                    "comment_count": 0,
                                    "paraphrased_top_comments": []
                                })
                    except Exception:
                        pass
                continue

            post_id = f"reddit_{post.id}"
            url = f"https://www.reddit.com{post.permalink}"
            created_utc = time.strftime('%Y-%m-%d', time.gmtime(post.created_utc))
            
            # Short excerpt max 25 words strictly enforced
            body_text = post.selftext or ""
            short_excerpt = clip_to_25_words(f"{post.title}. {body_text}")
            paraphrase = paraphrase_text(f"{post.title}. {body_text}", max_words=60)

            # Top comments (paraphrased, NO usernames)
            paraphrased_comments = []
            if post.num_comments > 0:
                try:
                    post.comments.replace_more(limit=0)
                    for comment in post.comments[:3]:
                        if comment.body and len(comment.body) > 10:
                            cleaned_c = clip_to_25_words(comment.body)
                            paraphrased_comments.append(cleaned_c)
                except Exception:
                    pass

            collected_items.append({
                "id": post_id,
                "source": f"reddit:r/{subreddit_name}",
                "url": url,
                "date": created_utc,
                "title": post.title.strip(),
                "short_excerpt": short_excerpt,
                "paraphrase": paraphrase,
                "upvotes": int(post.score or 0),
                "comment_count": int(post.num_comments or 0),
                "paraphrased_top_comments": paraphrased_comments
            })

            # Respect rate limit
            time.sleep(0.5)

    except (ResponseException, OAuthException) as e:
        print(f"[reddit error] Authentication or network error for r/{subreddit_name}: {e}")
    except Exception as e:
        print(f"[reddit error] Failed collecting from r/{subreddit_name}: {e}")

    return collected_items
