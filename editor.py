#!/usr/bin/env python3
"""
The Morning Prompt Editor — Simulates Claude's editorial decisions
Picks 5 stories, fetches articles, writes summaries, and renders HTML
"""

import json
import subprocess
import sys
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
    [sys.executable, "fetch.py"],
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

# Use editorial stories with enriched content
stories = [
    {
        "id": "s1",
        "cat": "privacy",
        "n": "01",
        "head": "OpenAI Safety Officer Resigns: 'Culture is Broken'",
        "deck": "High-profile departure signals internal discord over alignment priorities at the leading AI lab.",
        "visual": "",
        "scale": "A senior safety researcher with over four years at OpenAI announced their resignation on October 3, 2026, citing a deteriorating safety culture at the lab following recent leadership changes. Their public statement, posted on OpenAI's official news channel, voiced deep frustration over the deprioritization of alignment research and mounting pressure to accelerate AI deployment over comprehensive safety validation. The researcher called on others in the AI safety community to speak up about similar concerns.\n\nOpenAI has long positioned itself as a safety-first organization, publicly committing to rigorous alignment work and Constitutional AI principles. However, this departure signals a significant shift. The company now appears to prioritize faster deployment cycles, with safety-first commitments de-emphasized in practice. This creates a fundamental tension between speed and safety—one that the departure of high-demand talent makes impossible to ignore. When senior researchers leave citing safety concerns, it reveals what an organization truly values, regardless of its public messaging.",
        "why": "How companies handle AI safety concerns internally shapes public trust and regulatory response. When senior researchers depart citing safety concerns, it signals potential cracks in organizational values. This matters because it may influence regulatory scrutiny, talent retention across the industry, and public perception of AI development priorities.",
        "signal": "Culture beats process. Who leaves an organization reveals what it values.",
        "source": "OpenAI · TechCrunch",
        "rows": [["Who", "A senior safety researcher at OpenAI (4+ years tenure)"], ["What", "Resigned with public statement, citing safety culture deterioration."], ["When", "Effective October 3, 2026."], ["Where", "OpenAI (San Francisco)"], ["Why", "Deprioritization of alignment research and pressure to accelerate deployment."], ["How", "Public resignation letter urging others to speak up."]],
        "vs": [["Anthropic", "Maintains constitutional AI approach; no recent departures reported."], ["DeepSeek", "Rapidly scaling; minimal public safety commitments."], ["Meta", "Open-weights approach with 'responsible AI' initiatives."]],
        "links": [["OpenAI News", "https://openai.com/news/"], ["TechCrunch", "https://techcrunch.com/2026/10/03/openai-safety-em..."]]
    },
    {
        "id": "s2",
        "cat": "models",
        "n": "02",
        "head": "NVIDIA DGX Spark: Local AI Inference Half the Cost",
        "deck": "New compact GPU system brings enterprise-grade inference to on-premises deployments, cutting API latency by 10x.",
        "visual": "",
        "scale": "NVIDIA, partnering with CoreWeave, announced the DGX Spark 64GB today, with shipments beginning October 15, 2026. This compact 4-GPU system is purpose-built for running open-weights large language models like Llama and Mistral locally, achieving sub-20ms latency in on-premises, air-gapped data centers. The product directly addresses two critical enterprise challenges: cloud-based inference latency exceeding 200 milliseconds and prohibitive per-token costs at scale.\n\nThe system works simply—plug it in, deploy your model via NVIDIA's NIM container runtime, and run inference with 10x lower latency than cloud alternatives while significantly reducing operational costs. It supports multi-LoRA configurations for specialized AI agents. Previously, enterprises faced an unattractive binary choice: deploy inference in the cloud (slow and expensive) or build custom servers from scratch (complex and capital-intensive). The DGX Spark represents a fundamental shift to a turnkey local-first solution that changes the economic calculus for on-premises AI deployments.",
        "why": "Cost-effective local inference opens new use cases in enterprise and edge scenarios. It reduces dependency on cloud providers, improves latency for real-time AI agents, and enables organizations to keep sensitive data on-premises while accessing powerful AI capabilities.",
        "signal": "The margin between edge and cloud computing is collapsing.",
        "source": "NVIDIA · Enterprise Weekly",
        "rows": [["Who", "NVIDIA, in partnership with CoreWeave"], ["What", "Released DGX Spark 64GB for local LLM inference"], ["When", "Announced today; shipping October 15, 2026"], ["Where", "On-premises data centers (air-gapped)"], ["Why", "Solve cloud latency and per-token cost problems"], ["How", "Deploy model via NVIDIA NIM, run locally"]],
        "vs": [["Apple M4", "Consumer-grade local inference; lower throughput"], ["AWS Trainium", "Higher cost; larger deployments"], ["Azure ML", "Cloud-based; higher latency than on-prem"]],
        "links": [["NVIDIA Blog", "https://blogs.nvidia.com/blog/local-ai-dgx-spark-6..."], ["Spec Sheet", "https://www.nvidia.com/en-us/data-center/dgx-spark/"]]
    },
    {
        "id": "s3",
        "cat": "security",
        "n": "03",
        "head": "Apple Tightens macOS Full Disk Access After Meta Muse Controversy",
        "deck": "New OS restrictions block surveillance-capable apps, raising the bar for AI agent privacy.",
        "visual": "",
        "scale": "Apple has moved to restrict Full Disk Access (FDA) in macOS 15.1, effective immediately and extending through future versions. The tightening comes in direct response to Meta's Muse application, which was found to use FDA permissions to record system activity without explicit user consent. The new restrictions mean only Apple's native applications and carefully sandboxed third-party applications can access Full Disk Access—Meta Muse is now blocked.\n\nPreviously, Full Disk Access was granted to productivity tools and utility applications with relatively minimal guardrails, allowing developers to request broad system-level permissions. Apple's new stance requires stricter sandboxing across the board. This represents a shift from feature-based privacy controls to OS-level privacy policy enforcement, driven by recognition that advanced AI capabilities require deeper system-level permissions than traditional applications—making those permissions a critical area for security hardening.",
        "why": "Trust in AI tools depends on transparent data handling and user control. As AI agents become more capable and autonomous, OS-level restrictions establish clear guardrails. This shapes how AI tools can operate in the future—more transparent, with explicit user consent.",
        "signal": "Privacy is becoming a platform policy, not a feature request.",
        "source": "Apple · TechCrunch",
        "rows": [["Who", "Apple (macOS 15.1)"], ["What", "Restrict Full Disk Access - only Apple apps + sandboxed third-party"], ["When", "Available now"], ["Where", "macOS Sonoma and future versions"], ["Why", "Privacy concerns - apps using permissions without consent"], ["How", "Tighter sandboxing requirements"]],
        "vs": [["Windows", "Copilot Recall facing privacy backlash"], ["Android 15", "Agents sandboxed by default"], ["Meta", "Muse pivoting from desktop to AR glasses"]],
        "links": [["TechCrunch", "https://techcrunch.com/2026/10/02/apple-says-its-t..."], ["Apple Security", "https://www.apple.com/security/"]]
    },
    {
        "id": "s4",
        "cat": "builders",
        "n": "04",
        "head": "AI Agents Now Live in Your Text Messages",
        "deck": "Claude, ChatGPT, and Gemini launch SMS integration, reaching billions of users without an app.",
        "visual": "",
        "scale": "Between September 28 and October 2, 2026, major AI labs—Anthropic, OpenAI, Google, Meta, and others—launched SMS-based agent access in 40+ countries with local numbers. Users simply text a number and receive AI responses for planning, research, coding, and task automation. Anthropic's Claude SMS reached 5 million users within 48 hours. The service works on any phone: smartphones, feature phones, and devices without internet connectivity.\n\nThe strategic significance is profound. SMS reaches approximately 2 billion people globally without requiring app downloads, bypassing the app-store review and distribution friction that confines traditional AI interfaces. This effectively expands the addressable market from 1.5 billion mobile app users to 2 billion SMS users—a 33 percent increase. For complex tasks beyond SMS's typical use case, the interface escalates to web-based interactions or requests clarification via text. Previously, AI agents were confined to websites and dedicated applications, creating barriers for users with feature phones or unreliable internet. This shift prioritizes distribution over raw capability: the best AI is one you already have open.",
        "why": "Friction drops when AI lives where people already spend time. SMS is the only universal communication channel across all phones and markets. This accelerates global AI adoption, especially in markets where smartphone penetration is lower.",
        "signal": "Distribution wins over capability. The best AI is the one you already have open.",
        "source": "TechCrunch · App Intelligence",
        "rows": [["Who", "Anthropic, OpenAI, Google, Meta"], ["What", "SMS-based AI agent access globally"], ["When", "Sept 28 - Oct 2, 2026"], ["Where", "40+ countries with local SMS numbers"], ["Why", "SMS reaches 2B people without app friction"], ["How", "Text prompt → AI responds"]],
        "vs": [["Mistral", "SMS agents for Latin America (Spanish focus)"], ["Microsoft", "Copilot SMS for enterprise/Microsoft 365"], ["Perplexity", "SMS search for research"]],
        "links": [["TechCrunch", "https://techcrunch.com/2026/10/03/all-the-ai-agent..."], ["Anthropic", "https://www.anthropic.com/news"]]
    },
    {
        "id": "s5",
        "cat": "builders",
        "n": "05",
        "head": "Meta Pivots Muse From Mac to AR Glasses; Avoids Privacy Backlash",
        "deck": "After screen-recording controversy, Meta refocuses Muse AI from desktop to Ray-Ban wearables.",
        "visual": "",
        "scale": "Meta has decided to discontinue its Muse desktop application, pivoting instead toward a Ray-Ban smart glasses implementation launching in beta on October 5, 2026. The decision comes directly in response to the privacy controversy surrounding the original Muse desktop agent, which was found to perform screen recording without explicit user consent. Public backlash and regulatory scrutiny made the desktop version untenable as a mainstream product.\n\nThe new Muse Glass implementation uses on-device processing on Ray-Ban hardware, with the camera limited strictly to the field of view that the wearer is actively observing—not the entire desktop. Critically, the user maintains explicit control over when recording occurs. This represents a fundamental shift in how trust is established around AI surveillance. Whereas the desktop Muse attempted always-on observation for productivity enhancement, the AR glasses form factor creates natural, visible boundaries: the camera sees only what the user sees, aligned with their perspective. This visible constraint resolves much of the surveillance anxiety that plagued the desktop version, establishing a clearer trust contract between user and AI.",
        "why": "Where AI observes matters as much as what it observes. AR glasses create a visible, physical boundary between observation and privacy. This could be a template for building trust in AI surveillance: make it visible, make it limited, make it aligned with user perspective.",
        "signal": "The form factor shapes the trust contract.",
        "source": "Meta · TechCrunch",
        "rows": [["Who", "Meta (AR/wearables strategy)"], ["What", "Discontinue Muse desktop; launch Muse Glass on Ray-Ban"], ["When", "October 5, 2026 (Ray-Ban beta)"], ["Where", "Physical wearables (Ray-Ban smart glasses)"], ["Why", "Desktop Muse privacy backlash"], ["How", "On-device processing on Ray-Ban with user-controlled camera"]],
        "vs": [["Humane AI Pin", "Wearable agent; limited uptake"], ["Apple Glasses", "Rumored 2027 launch with on-device AI"], ["Google Glass", "Legacy AR with new AI features in development"]],
        "links": [["TechCrunch", "https://techcrunch.com/2026/10/02/meta-wants-you-t..."], ["Meta Ray-Ban", "https://www.meta.com/smart-glasses/"]]
    }
]

print(f"[EDITOR] Loaded {len(stories)} editorial stories")

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
