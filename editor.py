#!/usr/bin/env python3
"""
The Morning Prompt Editor — Simulates Claude's editorial decisions
Picks 5 stories, fetches articles, writes summaries, and renders HTML
"""

import json
import subprocess
from datetime import datetime
import os

# Get candidates from fetch.py
print("[EDITOR] Fetching candidates...")
result = subprocess.run(
    ["C:\\Users\\jaina\\anaconda3\\python.exe", "fetch.py"],
    capture_output=True,
    text=True,
    cwd=os.getcwd()
)

candidates_text = result.stdout
print(candidates_text)

# Hardcoded editorial decisions for demo
# (In the real skill, Claude would fetch articles and write these)
print("\n[EDITOR] Picking top 5 stories...")

stories = [
    {
        "id": "s1",
        "cat": "privacy",
        "n": "01",
        "head": "OpenAI Safety Officer Resigns: 'Culture is Broken'",
        "deck": "High-profile departure signals internal discord over alignment priorities at the leading AI lab.",
        "visual": "",
        "rows": [
            ["Who", "A senior safety researcher at OpenAI (4+ years tenure)"],
            ["What", "Resigned with public statement on company blog, claiming safety culture deteriorated after recent leadership changes."],
            ["When", "Effective October 3, 2026. Announcement posted this morning."],
            ["Where", "OpenAI (San Francisco); statement published on OpenAI's news page."],
            ["Why", "Researcher cited frustration with deprioritization of alignment research and pressure to accelerate deployment over safety validation."],
            ["How", "Public resignation letter urging others in AI safety to 'speak up' and align labs to shift focus back to safety."],
            ["Before → Now", "Before: OpenAI emphasized safety research post-GPT-5. Now: Departing safety researchers claim that's reversed."]
        ],
        "vs": [
            ["Anthropic", "Maintains constitutional AI approach; public commitment to safety-first development; no recent departures reported."],
            ["DeepSeek", "Rapidly scaling; minimal public safety commitments; focus on performance benchmarks."],
            ["Meta", "Open-weights approach; 'responsible AI' initiatives; some safety researchers joining competitors."]
        ],
        "links": [
            ["OpenAI News", "https://openai.com/news/"],
            ["TechCrunch Coverage", "https://techcrunch.com/2026/10/03/openai-safety-em..."]
        ]
    },
    {
        "id": "s2",
        "cat": "models",
        "n": "02",
        "head": "NVIDIA DGX Spark: Local AI Inference Half the Cost",
        "deck": "New compact GPU system brings enterprise-grade inference to on-premises deployments, cutting API latency by 10x.",
        "visual": "",
        "rows": [
            ["Who", "NVIDIA, in partnership with CoreWeave"],
            ["What", "Released DGX Spark 64GB—a 4-GPU system optimized for running open-weights LLMs (Llama, Mistral) with sub-20ms latency."],
            ["When", "Announced today; shipping October 15, 2026."],
            ["Where", "On-premises (data-center safe, fully air-gapped). Works with open-weights models."],
            ["Why", "Enterprises want local inference to avoid cloud API latency (200ms+) and per-token costs. DGX Spark cuts both."],
            ["How", "Plug in, deploy model, run inference via NVIDIA NIM container runtime. Multi-LoRA support for specialized agents."],
            ["Before → Now", "Before: Teams run inference in cloud (slow/expensive) or build custom servers (complex). Now: Turnkey local system designed for agentic workloads."]
        ],
        "vs": [
            ["Apple", "M4 Max MacBooks run 7B models locally; no API required; consumer-grade, lower throughput."],
            ["AWS Trainium", "Higher cost; designed for larger-scale deployments; more complex setup."],
            ["Azure ML", "Cloud-based inference; familiar to enterprises; higher latency than on-prem."]
        ],
        "links": [
            ["NVIDIA Blog", "https://blogs.nvidia.com/blog/local-ai-dgx-spark-6..."],
            ["NVIDIA DGX Spark Spec Sheet", "https://www.nvidia.com/en-us/data-center/dgx-spark/"]
        ]
    },
    {
        "id": "s3",
        "cat": "security",
        "n": "03",
        "head": "Apple Tightens macOS Full Disk Access After Meta Muse Controversy",
        "deck": "New OS restrictions block surveillance-capable apps, raising the bar for AI agent privacy.",
        "visual": "",
        "rows": [
            ["What", "macOS Sonoma 15.1 restricts Full Disk Access (FDA). Only Apple system apps and properly sandboxed third-party apps can read user files. Meta Muse now blocked."],
            ["Why", "Users reported Meta Muse recording screens without explicit consent. Apple's response: tighter gating on powerful APIs."]
        ],
        "vs": [
            ["Microsoft Windows", "Copilot Recall (live screen recording) faces backlash; launch delayed pending privacy clarity."],
            ["Google Android 15", "Agents sandboxed by default; requires per-app permissions."],
            ["Meta", "Muse pivot away from desktop toward AR glasses (Ray-Ban), where recording is explicit."]
        ],
        "links": [
            ["TechCrunch", "https://techcrunch.com/2026/10/02/apple-says-its-t..."],
            ["Apple Security & Privacy Updates", "https://www.apple.com/security/"]
        ]
    },
    {
        "id": "s4",
        "cat": "builders",
        "n": "04",
        "head": "AI Agents Now Live in Your Text Messages",
        "deck": "Claude, ChatGPT, and Gemini launch SMS integration, reaching billions of users without an app.",
        "visual": "",
        "rows": [
            ["Who", "Anthropic (Claude), OpenAI (ChatGPT), Google (Gemini), Meta (Llama agents)"],
            ["What", "Multiple AI companies launched SMS-based agent access. Text a number → interact with AI agents for planning, research, and task automation."],
            ["When", "Rolled out Sept 28 – Oct 2, 2026. Claude SMS reached 5M users in 48 hours."],
            ["Where", "Global SMS access. US: +1-415-CLAUDE-1. 40 countries with local numbers. No app download required."],
            ["Why", "SMS reaches 2B people without smartphones. Bypasses app-store review and distribution friction. Universal interface."],
            ["How", "Text a prompt. Agents respond with summaries, itineraries, code, research. For complex tasks, escalate to web or request clarification via SMS."],
            ["Before → Now", "Before: Agents required websites or apps. Now: Agents work on any phone, even feature phones (SMS only). Market expands from 1.5B app users to 2B SMS users."]
        ],
        "vs": [
            ["Mistral", "Launched Mistral Agents SMS (Latin America first); Spanish-language focus."],
            ["Microsoft", "Copilot SMS beta (enterprise/Microsoft 365 only); focused on Outlook/Teams tasks."],
            ["Perplexity", "SMS search: text research questions, get cited summaries."]
        ],
        "links": [
            ["TechCrunch", "https://techcrunch.com/2026/10/03/all-the-ai-agent..."],
            ["Anthropic Announcement", "https://www.anthropic.com/news"]
        ]
    },
    {
        "id": "s5",
        "cat": "builders",
        "n": "05",
        "head": "Meta Pivots Muse From Mac to AR Glasses; Avoids Privacy Backlash",
        "deck": "After screen-recording controversy, Meta refocuses Muse AI from desktop to Ray-Ban wearables.",
        "visual": "",
        "rows": [
            ["What", "Meta discontinued Muse desktop app; launching 'Muse Glass' beta on Ray-Ban smart glasses. On-device agents, no screen recording."],
            ["Why", "Desktop Muse faced backlash for full-screen recording without user consent. AR glasses offer agent access without privacy concerns."],
            ["When", "Muse Glass available to Ray-Ban beta users starting October 5, 2026."]
        ],
        "vs": [
            ["Humane AI Pin", "Wearable agent; limited uptake; exploring pivots."],
            ["Apple Glasses", "Rumored 2027 launch; expected on-device agent support."],
            ["Google Glass", "Legacy AR; new AI features in development."]
        ],
        "links": [
            ["TechCrunch", "https://techcrunch.com/2026/10/02/meta-wants-you-t..."],
            ["Meta Ray-Ban Smart Glasses", "https://www.meta.com/smart-glasses/"]
        ]
    }
]

word = {
    "term": "Agentic Loop",
    "pos": "noun · AI architecture",
    "def": "Repeating cycle where an AI observes the world, decides on actions, and executes them autonomously.",
    "why": "Foundation of next-generation AI systems that don't just respond but actively work on your behalf.",
    "tie": "Ties to Story #1 & #4: SMS agents and safety departures highlight how agentic systems are both increasingly powerful and increasingly controversial."
}

print(f"[EDITOR] Selected {len(stories)} stories for today's edition.")
print(f"[EDITOR] Word of the Day: {word['term']}")

# Build HTML
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Morning Prompt — Daily AI News</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #faf6eb;
            color: #1a1710;
            line-height: 1.6;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        .header {
            margin-bottom: 40px;
            border-bottom: 2px solid #d4a04a;
            padding-bottom: 20px;
        }

        .header h1 {
            font-size: 32px;
            font-weight: 700;
            color: #1a1710;
            margin-bottom: 8px;
        }

        .header .meta {
            font-size: 14px;
            color: #666;
        }

        .content {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 40px;
            margin-bottom: 40px;
        }

        .stories {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }

        .sidebar {
            padding: 20px;
            background: #2a1710;
            color: #faf6eb;
            border-radius: 8px;
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .story {
            border: 1px solid #e0d5c7;
            border-radius: 4px;
            padding: 0;
            overflow: hidden;
            transition: box-shadow 0.2s ease;
        }

        .story:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .story-header {
            padding: 20px;
            cursor: pointer;
            display: flex;
            align-items: flex-start;
            gap: 16px;
            background: #fef9f3;
        }

        .story-number {
            font-size: 28px;
            font-weight: 300;
            color: #d4a04a;
            min-width: 40px;
            opacity: 0.6;
            line-height: 1;
        }

        .story-header-content {
            flex: 1;
        }

        .story-cat {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            color: white;
            margin-bottom: 8px;
        }

        .story-headline {
            font-size: 18px;
            font-weight: 700;
            color: #1a1710;
            line-height: 1.3;
            margin-bottom: 8px;
        }

        .story-deck {
            font-size: 14px;
            color: #666;
            line-height: 1.4;
        }

        .story-body {
            display: none;
            padding: 20px;
            background: #fff;
            border-top: 1px solid #e0d5c7;
        }

        .story.expanded .story-body {
            display: block;
        }

        .story-rows {
            margin: 20px 0;
        }

        .story-row {
            display: grid;
            grid-template-columns: 120px 1fr;
            gap: 12px;
            margin-bottom: 12px;
            line-height: 1.5;
        }

        .story-row strong {
            color: #1a1710;
            font-weight: 600;
        }

        .story-row-value {
            color: #444;
        }

        .story-vs {
            margin: 20px 0;
            padding: 12px;
            background: #fef9f3;
            border-radius: 4px;
        }

        .story-vs-header {
            font-weight: 600;
            color: #1a1710;
            margin-bottom: 8px;
            font-size: 13px;
        }

        .story-vs-item {
            margin-bottom: 8px;
            font-size: 14px;
        }

        .story-vs-item strong {
            color: #1a1710;
        }

        .story-links {
            margin: 20px 0;
            padding: 12px;
            background: #fef9f3;
            border-radius: 4px;
        }

        .story-links-header {
            font-weight: 600;
            color: #1a1710;
            margin-bottom: 8px;
            font-size: 13px;
        }

        .story-link {
            display: block;
            margin-bottom: 6px;
        }

        .story-link a {
            color: #2a6fa8;
            text-decoration: none;
            font-size: 14px;
        }

        .story-link a:hover {
            text-decoration: underline;
        }

        .story-votes {
            margin-top: 16px;
            display: flex;
            gap: 8px;
        }

        .vote-btn {
            padding: 6px 12px;
            border: 1px solid #d4a04a;
            background: transparent;
            color: #1a1710;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s ease;
        }

        .vote-btn:hover {
            background: #d4a04a;
            color: #faf6eb;
        }

        .word-of-day h2 {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            color: #d4a04a;
            margin-bottom: 16px;
        }

        .word-card {
            background: #3a2710;
            padding: 16px;
            border-radius: 6px;
            color: #faf6eb;
        }

        .word-term {
            font-size: 20px;
            font-weight: 700;
            color: #d4a04a;
            margin-bottom: 8px;
        }

        .word-pos {
            font-size: 12px;
            color: #aaa;
            margin-bottom: 12px;
        }

        .word-def {
            font-size: 13px;
            line-height: 1.5;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid #5a4a3a;
        }

        .word-why {
            font-size: 12px;
            line-height: 1.5;
            margin-bottom: 12px;
        }

        .word-tie {
            font-size: 11px;
            color: #aaa;
            font-style: italic;
        }

        .story-toggle {
            display: none;
        }

        .story-toggle::after {
            content: " ▼";
            font-size: 12px;
        }

        .story.expanded .story-toggle::after {
            content: " ▲";
        }

        @media (max-width: 820px) {
            .content {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .sidebar {
                position: static;
            }

            .story-header {
                flex-direction: column;
                gap: 8px;
            }

            .story-number {
                min-width: auto;
            }

            .story-row {
                grid-template-columns: 1fr;
                gap: 4px;
            }

            .story-row strong::after {
                content: ": ";
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>The Morning Prompt</h1>
            <div class="meta">
                Daily AI news digest • Friday, October 3, 2026
            </div>
        </div>

        <div class="content">
            <div class="stories" id="stories"></div>
            <div class="sidebar">
                <div class="word-of-day">
                    <h2>Word of the Day</h2>
                    <div class="word-card" id="word-card"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const CATS = {
            privacy:  { label: "Agents & Privacy",    color: "#7a3ea0" },
            models:   { label: "Models",              color: "#2a6fa8" },
            security: { label: "Security",            color: "#b33425" },
            builders: { label: "Builders & Funding",  color: "#4db87a" }
        };

        const STORIES = %STORIES%;
        const WORD = %WORD%;

        function renderStories() {
            const container = document.getElementById('stories');
            STORIES.forEach((story, idx) => {
                const catInfo = CATS[story.cat] || { label: "News", color: "#999" };

                let rowsHtml = '';
                if (story.rows && story.rows.length > 0) {
                    rowsHtml = '<div class="story-rows">';
                    story.rows.forEach(([label, value]) => {
                        rowsHtml += `
                            <div class="story-row">
                                <strong>${label}</strong>
                                <div class="story-row-value">${value}</div>
                            </div>
                        `;
                    });
                    rowsHtml += '</div>';
                }

                let vsHtml = '';
                if (story.vs && story.vs.length > 0) {
                    vsHtml = '<div class="story-vs"><div class="story-vs-header">🥊 What Others Are Doing</div>';
                    story.vs.forEach(([company, line]) => {
                        vsHtml += `<div class="story-vs-item"><strong>${company}:</strong> ${line}</div>`;
                    });
                    vsHtml += '</div>';
                }

                let linksHtml = '';
                if (story.links && story.links.length > 0) {
                    linksHtml = '<div class="story-links"><div class="story-links-header">Source Links</div>';
                    story.links.forEach(([label, url]) => {
                        linksHtml += `<div class="story-link"><a href="${url}" target="_blank">${label}</a></div>`;
                    });
                    linksHtml += '</div>';
                }

                const storyHtml = `
                    <div class="story ${idx === 0 ? 'expanded' : ''}">
                        <div class="story-header" onclick="toggleStory(${idx})">
                            <div class="story-number">${story.n}</div>
                            <div class="story-header-content">
                                <div class="story-cat" style="background-color: ${catInfo.color};">${catInfo.label}</div>
                                <div class="story-headline">${story.head}</div>
                                <div class="story-deck">${story.deck}</div>
                            </div>
                            <span class="story-toggle"></span>
                        </div>
                        <div class="story-body">
                            ${story.visual ? `<div class="story-visual">${story.visual}</div>` : ''}
                            <a href="${story.links && story.links[0] ? story.links[0][1] : '#'}" target="_blank" style="color: #2a6fa8; text-decoration: none; font-weight: 600;">Read full story →</a>
                            ${rowsHtml}
                            ${vsHtml}
                            ${linksHtml}
                            <div class="story-votes">
                                <button class="vote-btn" onclick="voteStory(${idx}, 'up')">👍 More like this</button>
                                <button class="vote-btn" onclick="voteStory(${idx}, 'down')">👎 Less</button>
                            </div>
                        </div>
                    </div>
                `;

                container.innerHTML += storyHtml;
            });
        }

        function renderWord() {
            const container = document.getElementById('word-card');
            if (!WORD.term) return;
            container.innerHTML = `
                <div class="word-term">${WORD.term}</div>
                <div class="word-pos">${WORD.pos}</div>
                <div class="word-def">${WORD.def}</div>
                <div class="word-why"><strong>Why it matters:</strong> ${WORD.why}</div>
                <div class="word-tie">${WORD.tie}</div>
            `;
        }

        function toggleStory(idx) {
            const stories = document.querySelectorAll('.story');
            stories[idx].classList.toggle('expanded');
        }

        function voteStory(idx, type) {
            console.log(`Vote: ${type} on story ${idx}`);
        }

        window.addEventListener('DOMContentLoaded', () => {
            renderStories();
            renderWord();
        });
    </script>
</body>
</html>
"""

# Inject data into HTML
html = html.replace("%STORIES%", json.dumps(stories))
html = html.replace("%WORD%", json.dumps(word))

# Write to output
output_file = f"output/{datetime.now().strftime('%Y-%m-%d')}.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n[EDITOR] [OK] Edition rendered to {output_file}")
print(f"[EDITOR] Open in browser to view: file://{os.path.abspath(output_file)}")

# Save to Supabase
print("\n[EDITOR] Saving to Supabase...")
try:
    from supabase_client import get_supabase_client
    from datetime import date

    supabase = get_supabase_client()

    if supabase.enabled:
        # Create edition
        edition_id = supabase.create_edition(
            date.today(),
            headline="Top 5 AI Stories",
            description=f"Daily AI news digest for {date.today()}"
        )

        if edition_id:
            # Store each story
            for story in stories:
                supabase.store_story(edition_id, story)
                print(f"  [OK] Stored: {story['head'][:60]}...")

            print(f"[SUPABASE] Edition {edition_id} saved successfully!")
    else:
        print("[WARN] Supabase not configured. Run won't be saved to database.")
except Exception as e:
    print(f"[SUPABASE] Error saving to database: {e}")
    print("[WARN] HTML edition still created successfully")
