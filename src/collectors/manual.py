# src/collectors/manual.py — Manual File Import Collector (Tier 3)
# Usage: from src.collectors.manual import import_manual_files
# Requires: csv, os, hashlib
#
# Gotchas:
# - Usernames in CSV headers or rows must be ignored or stripped immediately.
# - Text files may contain pasted LinkedIn comments; clip to 25 words max excerpt.

import os
import csv
import hashlib
import time
from typing import List, Dict, Any
from src.db import clip_to_25_words

def process_manual_text_file(filepath: str) -> List[Dict[str, Any]]:
    items = []
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()
    
    # Blocks separated by double newlines or lines starting with '---'
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    for idx, block in enumerate(blocks):
        lines = block.splitlines()
        title = lines[0][:80].strip() if lines else "Manual Note"
        body = " ".join(lines[1:]).strip() if len(lines) > 1 else lines[0]
        
        item_id = f"manual_{hashlib.md5(f'{filename}_{idx}_{block}'.encode('utf-8')).hexdigest()[:12]}"
        short_excerpt = clip_to_25_words(f"{title}. {body}")
        
        items.append({
            "id": item_id,
            "source": f"manual:{filename}",
            "url": f"file://data/imports/{filename}#item{idx+1}",
            "date": time.strftime('%Y-%m-%d'),
            "title": title,
            "short_excerpt": short_excerpt,
            "paraphrase": clip_to_25_words(body) or title,
            "upvotes": 0,
            "comment_count": 0,
            "paraphrased_top_comments": []
        })
    return items

def process_manual_csv_file(filepath: str) -> List[Dict[str, Any]]:
    items = []
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            # Normalize headers
            row_lower = {k.lower().strip(): v.strip() for k, v in row.items() if k and v}
            title = row_lower.get("title") or row_lower.get("headline") or row_lower.get("subject") or f"Item {idx+1}"
            body = row_lower.get("comment") or row_lower.get("body") or row_lower.get("text") or row_lower.get("review") or ""
            url = row_lower.get("url") or row_lower.get("link") or f"file://data/imports/{filename}#row{idx+2}"
            date_str = row_lower.get("date") or time.strftime('%Y-%m-%d')
            upvotes = int(row_lower.get("upvotes") or row_lower.get("likes") or 0)
            
            # Enforce privacy: never capture author or username columns
            item_id = f"manual_csv_{hashlib.md5(f'{filename}_{idx}_{url}'.encode('utf-8')).hexdigest()[:12]}"
            short_excerpt = clip_to_25_words(f"{title}. {body}")

            items.append({
                "id": item_id,
                "source": f"manual:{filename}",
                "url": url,
                "date": date_str,
                "title": title[:100],
                "short_excerpt": short_excerpt,
                "paraphrase": clip_to_25_words(body) or title,
                "upvotes": upvotes,
                "comment_count": 0,
                "paraphrased_top_comments": []
            })
    return items

def import_manual_files(imports_dir: str = "data/imports") -> List[Dict[str, Any]]:
    """Scans the manual imports directory and processes all CSV and TXT files."""
    os.makedirs(imports_dir, exist_ok=True)
    all_items = []
    
    for fname in os.listdir(imports_dir):
        fpath = os.path.join(imports_dir, fname)
        if not os.path.isfile(fpath):
            continue
            
        ext = os.path.splitext(fname)[1].lower()
        if ext == ".csv":
            all_items.extend(process_manual_csv_file(fpath))
        elif ext in [".txt", ".md"]:
            all_items.extend(process_manual_text_file(fpath))
            
    return all_items
