# src/db.py — SQLite storage layer for Sayari Research Tool
# Usage: imported by collectors and analysis pipeline
# Requires: sqlite3 (standard library)
#
# Gotchas:
# - Privacy rule strictly enforced: never store author username or profile metadata.
# - Word limit rule strictly enforced: short_excerpt is clipped to max 25 words.

import sqlite3
import json
import os
import re
import html
from typing import Dict, Any, List, Optional

def get_db_connection(db_path: str = "data/sayari.db") -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = "data/sayari.db"):
    """Initializes tables for raw items, ideas, glossary, and blocked sources."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS raw_items (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        url TEXT NOT NULL,
        date TEXT,
        title TEXT NOT NULL,
        short_excerpt TEXT NOT NULL,
        paraphrase TEXT,
        upvotes INTEGER DEFAULT 0,
        comment_count INTEGER DEFAULT 0,
        paraphrased_top_comments TEXT,
        theme TEXT,
        emotion TEXT,
        intensity INTEGER DEFAULT 1,
        post_type TEXT,
        audience TEXT,
        used_terms TEXT,
        passed_filters INTEGER DEFAULT 1,
        drop_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        format TEXT NOT NULL,
        pillar TEXT NOT NULL,
        hook TEXT NOT NULL,
        suggested_visual TEXT NOT NULL,
        extends_idea TEXT NOT NULL,
        evidence_sources TEXT NOT NULL,
        source_count INTEGER DEFAULT 0,
        avg_intensity REAL DEFAULT 1.0,
        engagement_score REAL DEFAULT 0.0,
        risks TEXT NOT NULL,
        verify_before_use TEXT NOT NULL,
        rank_score REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS glossary (
        term TEXT PRIMARY KEY,
        frequency INTEGER DEFAULT 1,
        source_count INTEGER DEFAULT 1,
        paraphrased_contexts TEXT,
        is_vendor_marketing_only INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS blocked_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_name TEXT NOT NULL,
        url TEXT NOT NULL,
        reason TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        trigger_type TEXT NOT NULL,
        sources_swept TEXT NOT NULL,
        time_ranges TEXT NOT NULL,
        raw_collected_count INTEGER DEFAULT 0,
        passed_filters_count INTEGER DEFAULT 0,
        dropped_noise_count INTEGER DEFAULT 0,
        summary_learnings TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

def record_pipeline_run(
    conn: sqlite3.Connection,
    trigger_type: str,
    sources_swept: str,
    time_ranges: str,
    raw_collected_count: int,
    passed_filters_count: int,
    dropped_noise_count: int,
    summary_learnings: str
) -> int:
    """Logs an execution run of the listening agent with source ranges and overall learnings in IST (UTC+5:30)."""
    from datetime import datetime, timezone, timedelta
    cur = conn.cursor()
    IST = timezone(timedelta(hours=5, minutes=30))
    ts = datetime.now(timezone.utc).astimezone(IST).strftime('%Y-%m-%d %H:%M:%S IST')
    cur.execute("""
    INSERT INTO pipeline_runs (
        timestamp, trigger_type, sources_swept, time_ranges,
        raw_collected_count, passed_filters_count, dropped_noise_count, summary_learnings
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, trigger_type, sources_swept, time_ranges, raw_collected_count, passed_filters_count, dropped_noise_count, summary_learnings))
    conn.commit()
    return cur.lastrowid

def get_recent_pipeline_runs(conn: sqlite3.Connection, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves the recent pipeline execution history."""
    cur = conn.cursor()
    cur.execute("""
    SELECT id, timestamp, trigger_type, sources_swept, time_ranges,
           raw_collected_count, passed_filters_count, dropped_noise_count, summary_learnings
    FROM pipeline_runs
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    return [dict(r) for r in cur.fetchall()]

def clean_html_text(text: str) -> str:
    """Strips raw HTML tags and decodes HTML entities."""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = html.unescape(clean)
    return " ".join(clean.split())

def clip_to_25_words(text: str) -> str:
    """Strictly strips HTML and clips text to at most 25 words to comply with copyright & fair excerpt rules."""
    if not text:
        return ""
    cleaned = clean_html_text(text)
    words = cleaned.split()
    if len(words) <= 25:
        return " ".join(words)
    return " ".join(words[:25]) + "..."

def insert_raw_item(conn: sqlite3.Connection, item: Dict[str, Any]) -> bool:
    """Inserts a raw item if not already present. Enforces privacy and excerpt word limit."""
    cur = conn.cursor()
    short_excerpt = clip_to_25_words(item.get("short_excerpt", ""))
    used_terms_json = json.dumps(item.get("used_terms", [])) if isinstance(item.get("used_terms"), list) else item.get("used_terms", "[]")
    comments_json = json.dumps(item.get("paraphrased_top_comments", [])) if isinstance(item.get("paraphrased_top_comments"), list) else item.get("paraphrased_top_comments", "[]")

    try:
        cur.execute("""
        INSERT INTO raw_items (
            id, source, url, date, title, short_excerpt, paraphrase,
            upvotes, comment_count, paraphrased_top_comments, theme,
            emotion, intensity, post_type, audience, used_terms,
            passed_filters, drop_reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            upvotes=excluded.upvotes,
            comment_count=excluded.comment_count,
            paraphrased_top_comments=excluded.paraphrased_top_comments,
            theme=COALESCE(excluded.theme, raw_items.theme),
            emotion=COALESCE(excluded.emotion, raw_items.emotion),
            intensity=COALESCE(excluded.intensity, raw_items.intensity),
            post_type=COALESCE(excluded.post_type, raw_items.post_type),
            audience=COALESCE(excluded.audience, raw_items.audience),
            used_terms=COALESCE(excluded.used_terms, raw_items.used_terms),
            passed_filters=excluded.passed_filters,
            drop_reason=excluded.drop_reason
        """, (
            item["id"],
            item["source"],
            item["url"],
            item.get("date", ""),
            item.get("title", ""),
            short_excerpt,
            item.get("paraphrase", ""),
            item.get("upvotes", 0),
            item.get("comment_count", 0),
            comments_json,
            item.get("theme", None),
            item.get("emotion", None),
            item.get("intensity", 1),
            item.get("post_type", None),
            item.get("audience", None),
            used_terms_json,
            1 if item.get("passed_filters", True) else 0,
            item.get("drop_reason", "")
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[db error] insert_raw_item failed: {e}")
        return False

def log_blocked_source(conn: sqlite3.Connection, source_name: str, url: str, reason: str):
    """Logs blocked or paywalled sources that could not be accessed legitimately."""
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO blocked_sources (source_name, url, reason)
    VALUES (?, ?, ?)
    """, (source_name, url, reason))
    conn.commit()
