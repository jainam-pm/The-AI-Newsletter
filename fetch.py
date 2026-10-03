#!/usr/bin/env python3
"""
The Morning Prompt — Fetch and Score News Candidates
Zero LLM tokens. Pure Python. Runs before Claude sees candidates.
"""

import feedparser
import requests
import json
import yaml
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import defaultdict
import sys

# Configuration
CONFIG_FILE = "sources.yaml"
PUBLISHED_FILE = "published.json"
SEEN_FILE = "seen.json"
HOURS_BACK = 24
MAX_CANDIDATES = 25

# Load memory
def load_published():
    """Load published.json (last 30 days of stories)."""
    try:
        with open(PUBLISHED_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_seen():
    """Load seen.json (URLs already processed)."""
    try:
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_sources():
    """Load sources.yaml."""
    try:
        with open(CONFIG_FILE, "r") as f:
            data = yaml.safe_load(f)
            return data.get("sources", [])
    except FileNotFoundError:
        print("ERROR: sources.yaml not found", file=sys.stderr)
        return []

# Fetching
def fetch_rss(url):
    """Fetch RSS feed and return items."""
    try:
        feed = feedparser.parse(url)
        return feed.get("entries", [])
    except Exception as e:
        print(f"[WARN] RSS fetch failed: {url} - {e}", file=sys.stderr)
        return []

def fetch_api_hacker_news():
    """Fetch top HN stories from Algolia API."""
    try:
        url = "https://hn.algolia.com/api/v1/search"
        params = {
            "query": "AI",
            "tags": "story",
            "hitsPerPage": 50,
        }
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        items = []
        for hit in data.get("hits", []):
            items.append({
                "title": hit.get("title", ""),
                "link": hit.get("url", ""),
                "published": hit.get("created_at", ""),
                "score": hit.get("points", 0),
                "source": "hacker_news"
            })
        return items
    except Exception as e:
        print(f"[WARN] HN API fetch failed: {e}", file=sys.stderr)
        return []

# Deduplication
def normalize_url(url):
    """Normalize URL for comparison."""
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}".lower().rstrip("/")

def fuzzy_title_match(title1, title2, threshold=0.8):
    """Simple fuzzy match on titles (token overlap)."""
    try:
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, title1.lower(), title2.lower()).ratio()
        return ratio > threshold
    except:
        return title1.lower() == title2.lower()

# Scoring
def score_story(story, published_urls, source_count):
    """Score a story based on coverage, source, engagement."""
    score = 0

    # Multi-source boost
    if source_count >= 3:
        score += 3
    elif source_count == 2:
        score += 1

    # Official announcement boost
    if story.get("source") in ["openai", "google_ai", "meta_ai", "nvidia", "mistral", "hugging_face"]:
        score += 2

    # Engagement boost (HN/Reddit)
    hn_score = story.get("score", 0)
    if hn_score > 200:
        score += 2

    reddit_score = story.get("reddit_score", 0)
    if reddit_score > 500:
        score += 2

    # Major publication boost
    major_pubs = ["techcrunch", "venturebeat", "theverge", "technologyreview", "ars", "wired"]
    domain = urlparse(story.get("link", "")).netloc.lower()
    if any(pub in domain for pub in major_pubs):
        score += 1

    # Single minor source penalty
    if source_count == 1 and story.get("source") not in ["openai", "google_ai", "meta_ai"]:
        score -= 1

    return max(0, score)

# Main pipeline
def main():
    """Main fetch and score pipeline."""
    print("[INFO] Starting fetch...", file=sys.stderr)

    sources = load_sources()
    published = load_published()
    seen = load_seen()
    published_urls = set(s["url"] for s in published)

    # Track all items by normalized URL
    stories = defaultdict(lambda: {
        "urls": [],
        "titles": [],
        "sources": [],
        "scores": [],
        "published": None,
        "company": None,
        "follow_up": None
    })

    cutoff = datetime.utcnow() - timedelta(hours=HOURS_BACK)

    # Fetch from each source
    for source in sources:
        if source.get("type") == "rss":
            items = fetch_rss(source["url"])
            for item in items:
                link = item.get("link") or item.get("id", "")
                if not link:
                    continue

                title = item.get("title", "")
                published_str = item.get("published", "")

                # Normalize and deduplicate
                normalized = normalize_url(link)

                # Skip if already seen
                if link in seen:
                    continue

                stories[normalized]["urls"].append(link)
                stories[normalized]["titles"].append(title)
                stories[normalized]["sources"].append(source["name"])
                stories[normalized]["published"] = published_str

        elif source.get("type") == "api" and "hacker_news" in source["name"].lower():
            items = fetch_api_hacker_news()
            for item in items:
                link = item.get("link", "")
                if not link:
                    continue

                title = item.get("title", "")
                normalized = normalize_url(link)

                if link in seen:
                    continue

                stories[normalized]["urls"].append(link)
                stories[normalized]["titles"].append(title)
                stories[normalized]["sources"].append("Hacker News")
                stories[normalized]["scores"].append(item.get("score", 0))
                stories[normalized]["published"] = item.get("published", "")

    # Build candidates with scoring
    candidates = []
    for normalized, data in stories.items():
        # Pick primary URL (first seen)
        primary_url = data["urls"][0]
        primary_title = data["titles"][0]
        source_count = len(set(data["sources"]))

        # Check if follow-up
        follow_up_flag = None
        for published_item in published:
            if published_item["url"] == primary_url:
                # Exact match — skip (already covered)
                continue
            # Fuzzy match on company + product
            if fuzzy_title_match(primary_title, published_item["headline"], threshold=0.7):
                published_date = published_item.get("date", "")
                follow_up_flag = f"covered {published_date}"
                break

        # Score
        story_obj = {
            "link": primary_url,
            "title": primary_title,
            "source": data["sources"][0],
            "score": max(data["scores"]) if data["scores"] else 0
        }
        score = score_story(story_obj, published_urls, source_count)

        candidate = {
            "title": primary_title,
            "link": primary_url,
            "source": data["sources"][0],
            "sources_count": source_count,
            "score": score,
            "follow_up": follow_up_flag,
            "summary": f"Covered by {source_count} sources"
        }

        candidates.append(candidate)

    # Sort by score, then by source authority
    candidates.sort(key=lambda x: (-x["score"], -x["sources_count"]))

    # Output top candidates
    print("\nCANDIDATES (top 25):\n")
    for i, cand in enumerate(candidates[:MAX_CANDIDATES], 1):
        flag = f" | {cand['follow_up'].upper()}" if cand["follow_up"] else " | FRESH"
        print(f"{i}. [score:{cand['score']}] {cand['title'][:70]} | {cand['source'][:20]} | {cand['link'][:50]}... | {cand['summary']}{flag}")

    if not candidates:
        print("[WARN] No candidates found. Check sources.yaml and network.", file=sys.stderr)

if __name__ == "__main__":
    main()
