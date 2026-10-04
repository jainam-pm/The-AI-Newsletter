#!/usr/bin/env python3
"""
The Morning Prompt Editor — Simulates Claude's editorial decisions
Picks 5 stories, fetches articles, writes summaries, and renders HTML
"""

import json
import subprocess
from datetime import datetime, date
import os
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================================
# TIMING INSTRUMENTATION
# ============================================================================
timers = {}

def start_timer(label):
    """Start a timer for a section."""
    timers[label] = {"start": time.time(), "elapsed": None}

def end_timer(label):
    """End a timer and calculate elapsed time."""
    if label in timers:
        timers[label]["elapsed"] = time.time() - timers[label]["start"]
        return timers[label]["elapsed"]
    return 0

def print_timers():
    """Print all timing results in the specified format."""
    # Aggregate main timers only (exclude per-story timers for main report)
    main_timers = {k: v for k, v in timers.items() if not k.startswith("story_")}
    total = sum(t.get("elapsed", 0) for t in main_timers.values() if t.get("elapsed") is not None)
    timer_str = ", ".join(
        f"{label.capitalize()}: {t['elapsed']:.1f}s"
        for label, t in sorted(main_timers.items())
        if t.get("elapsed") is not None
    )
    print(f"\n[TIMER] {timer_str}, Total: {total:.1f}s")

# ============================================================================
# TASK 1 & 2: FETCH & PARSE CANDIDATES
# ============================================================================
print("[EDITOR] Fetching candidates...")
start_timer("fetch")

result = subprocess.run(
    ["C:\\Users\\jaina\\anaconda3\\python.exe", "fetch.py"],
    capture_output=True,
    text=True,
    cwd=os.getcwd()
)

fetch_elapsed = end_timer("fetch")
candidates_text = result.stdout
print(candidates_text)

# ============================================================================
# PARSE CANDIDATES FROM FETCH.PY OUTPUT
# ============================================================================
print("\n[EDITOR] Parsing and selecting top 5 stories...")
start_timer("selection")

def parse_candidates(candidates_text):
    """
    Parse candidates text from fetch.py.
    Format: "N. [score:X] title | source | link | summary | flag"
    """
    candidates = []
    lines = candidates_text.split("\n")

    for line in lines:
        # Skip header lines and empty lines
        if not line.strip() or "CANDIDATES" in line or "top 25" in line:
            continue

        # Match pattern: number. [score:X] title | source | link | summary | flag
        match = re.match(r"(\d+)\.\s*\[score:(\d+)\]\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+)", line)
        if match:
            idx, score, title, source, link, summary, flag = match.groups()

            # Extract sources_count from summary text (e.g., "Covered by 2 sources")
            sources_count = 1
            sources_match = re.search(r"Covered by (\d+) sources?", summary)
            if sources_match:
                sources_count = int(sources_match.group(1))

            candidates.append({
                "idx": int(idx),
                "score": int(score),
                "title": title.strip(),
                "source": source.strip(),
                "link": link.strip(),
                "summary": summary.strip(),
                "sources_count": sources_count,
                "flag": flag.strip(),
                "freshness": 1 if "FRESH" in flag else 0  # Higher score for fresh stories
            })

    return candidates

candidates = parse_candidates(candidates_text)
print(f"[EDITOR] Parsed {len(candidates)} candidates")

# ============================================================================
# SELECT TOP 5 BY RELEVANCE
# ============================================================================
# Relevance = score + freshness bonus
def select_top_stories(candidates, num=5):
    """Select top N stories by relevance (score + freshness)."""
    if not candidates:
        return []

    # Score + freshness bonus
    for c in candidates:
        c["relevance"] = c["score"] + (c["freshness"] * 2)  # Fresh stories get +2 boost

    sorted_candidates = sorted(candidates, key=lambda x: x["relevance"], reverse=True)
    return sorted_candidates[:num]

top_stories = select_top_stories(candidates, num=5)
selection_elapsed = end_timer("selection")

print(f"[EDITOR] Selected {len(top_stories)} stories for today's edition")

# ============================================================================
# CONVERT CANDIDATES TO STORY OBJECTS
# ============================================================================
# Map categories based on keywords in title/summary
CATEGORY_KEYWORDS = {
    "privacy": ["privacy", "safety", "ethics", "align"],
    "models": ["model", "llm", "gpu", "inference", "training", "weight"],
    "security": ["security", "breach", "cyber", "attack", "vulnerability", "access"],
    "builders": ["agent", "startup", "funding", "sms", "launch", "build"]
}

def guess_category(title, summary):
    """Guess story category from title and summary."""
    text = (title + " " + summary).lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return cat
    return "models"  # Default category

# Build story objects from candidates
stories = []
for i, cand in enumerate(top_stories, 1):
    cat = guess_category(cand["title"], cand["summary"])
    story = {
        "id": f"s{i}",
        "cat": cat,
        "n": f"{i:02d}",
        "head": cand["title"],
        "deck": cand["summary"],
        "visual": "",
        "scale": f"{cand['summary']} [From: {cand['source']}]",  # Use summary as placeholder for scale
        "why": f"Story from {cand['source']} covered by {cand['sources_count']} sources.",
        "signal": "Real-world AI signal.",
        "source": cand["source"],
        "rows": [
            ["Title", cand["title"]],
            ["Source", cand["source"]],
            ["Relevance Score", str(cand["score"])],
            ["Coverage", f"{cand.get('sources_count', 1)} sources"]
        ],
        "vs": [],
        "links": [
            ["Read Story", cand["link"]]
        ]
    }
    stories.append(story)

print(f"[EDITOR] Converted {len(stories)} candidates to story objects")

# ============================================================================
# WORD OF THE DAY (No hardcoding, just rotation)
# ============================================================================
print("[EDITOR] Loading Word of the Day list...")
try:
    with open("words_of_day.json", "r") as f:
        words_list = json.load(f)

    today = str(date.today())
    # Check if today's word already selected (prevent multiple runs per day from overwriting)
    todays_word = None
    for w in words_list:
        if w.get("last_used") == today:
            todays_word = w
            break

    # If today's word already selected, use it. Otherwise pick a new one
    if todays_word:
        word = todays_word
    else:
        # Find first word that wasn't used today
        word = None
        for w in words_list:
            last_used = w.get("last_used", "2000-01-01")
            if last_used != today:
                word = w
                w["last_used"] = today
                break

        # If all words used today (shouldn't happen - 8 words per day), pick oldest
        if not word:
            word = min(words_list, key=lambda w: w.get("last_used", "2000-01-01"))
            word["last_used"] = today

    # Update the file
    with open("words_of_day.json", "w") as f:
        json.dump(words_list, f, indent=2)

    print(f"[EDITOR] Word of the Day: {word['term']} (rotated, not repeating)")
except Exception as e:
    print(f"[WARN] Could not load words list: {e}. Using default.")
    word = {
        "term": "Agentic Loop",
        "pos": "noun · AI architecture",
        "def": "Repeating cycle where an AI observes the world, decides on actions, and executes them autonomously.",
        "why": "Foundation of next-generation AI systems that don't just respond but actively work on your behalf.",
        "tie": "Ties to Story #1 & #4: SMS agents and safety departures highlight how agentic systems are both increasingly powerful and increasingly controversial."
    }

# ============================================================================
# TASK 3: RENDER HTML (with timing)
# ============================================================================
print("[EDITOR] Rendering HTML newsletter...")
start_timer("render")

# Load newsletter template
try:
    with open("newsletter-template.html", "r", encoding="utf-8") as f:
        html = f.read()
except Exception as e:
    print(f"[ERROR] Could not load newsletter template: {e}")
    exit(1)

# Prepare story data without fake vote counts
stories_for_template = []
for story in stories:
    s = story.copy()
    # Remove any vote counts - they'll be fetched from Supabase
    s.pop('upvotes', None)
    s.pop('downvotes', None)
    stories_for_template.append(s)

# Prepare word data (remove last_used - not needed in template)
word_for_template = {
    "term": word["term"],
    "pos": word["pos"],
    "def": word["def"],
    "why": word["why"],
    "tie": word["tie"]
}

# Inject data into template using JSON.dumps (minimal JSON injection)
stories_json = json.dumps(stories_for_template)
word_json = json.dumps(word_for_template)

# Simple string replacement (already optimal)
html = html.replace("%STORIES%", stories_json)
html = html.replace("%WORD%", word_json)

render_elapsed = end_timer("render")

# Write to output (use newsletter-final.html as the destination)
output_file = "output/newsletter-final.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n[EDITOR] [OK] Edition rendered to {output_file}")
print(f"[EDITOR] Open in browser to view: file://{os.path.abspath(output_file)}")

# ============================================================================
# SAVE TO SUPABASE (with timing per story + total)
# ============================================================================
print("\n[EDITOR] Saving to Supabase...")
start_timer("supabase")

try:
    from supabase_client import get_supabase_client
    from datetime import date

    supabase = get_supabase_client()

    if supabase.enabled:
        # Check if edition already exists for today
        existing = supabase.client.table("editions").select("id").eq("date", str(date.today())).execute()

        if existing.data:
            # Edition exists, reuse it
            edition_id = existing.data[0]['id']
            print(f"[SUPABASE] Reusing existing edition {edition_id} for {date.today()}")
        else:
            # Create new edition
            edition_id = supabase.create_edition(
                date.today(),
                headline="Top 5 AI Stories",
                description=f"Daily AI news digest for {date.today()}"
            )

        if edition_id:
            # Delete old stories for this edition (if re-running)
            supabase.client.table("stories").delete().eq("edition_id", edition_id).execute()
            print(f"[SUPABASE] Cleared old stories for edition {edition_id}")

            # Store each story (with individual timing)
            # Save stories in parallel (up to 3 concurrent)
            def save_story_wrapper(story):
                story_timer_key = f"story_{story['id']}"
                start_timer(story_timer_key)
                try:
                    supabase.store_story(edition_id, story)
                    end_timer(story_timer_key)
                    return (True, story, timers[story_timer_key]['elapsed'])
                except Exception as e:
                    end_timer(story_timer_key)
                    return (False, story, timers[story_timer_key]['elapsed'])

            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(save_story_wrapper, s): s for s in stories}
                for future in as_completed(futures):
                    success, story, elapsed = future.result()
                    if success:
                        print(f"  [OK] Stored: {story['head'][:60]}... ({elapsed:.3f}s)")
                    else:
                        print(f"  [ERROR] Failed to store: {story['head'][:60]}...")

            print(f"[SUPABASE] Edition {edition_id} saved successfully!")
    else:
        print("[WARN] Supabase not configured. Run won't be saved to database.")

    supabase_elapsed = end_timer("supabase")
except Exception as e:
    print(f"[SUPABASE] Error saving to database: {e}")
    print("[WARN] HTML edition still created successfully")
    supabase_elapsed = end_timer("supabase")

# Update published.json to avoid re-publishing same stories
try:
    published_file = "published.json"
    published = []
    if os.path.exists(published_file):
        with open(published_file, "r") as f:
            published = json.load(f)

    today = str(date.today())
    # Remove any existing entries for today (avoid duplicates)
    published = [p for p in published if p.get("date") != today]

    # Add today's stories (one entry per story)
    for story in stories:
        published.append({
            "url": story.get("links", [["", ""]])[0][1] if story.get("links") else "",
            "headline": story["head"],
            "date": today
        })

    with open(published_file, "w") as f:
        json.dump(published, f, indent=2)

    print(f"[EDITOR] Updated published.json with {len(stories)} stories for {today}")
except Exception as e:
    print(f"[WARN] Failed to update published.json: {e}")

# ============================================================================
# PRINT FINAL TIMING REPORT
# ============================================================================
print_timers()
