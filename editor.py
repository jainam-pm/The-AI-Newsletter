#!/usr/bin/env python3
"""
The Morning Prompt Editor — Simulates Claude's editorial decisions
Picks 5 stories, fetches articles, writes summaries, and renders HTML
"""

import json
import subprocess
from datetime import datetime, date
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
        "scale": "WHO: A senior safety researcher with 4+ years tenure at OpenAI, a leading AI research organization known for developing GPT models. WHAT: This researcher publicly resigned, citing deteriorating safety culture within the organization following recent leadership changes. WHEN: October 3, 2026 - announced this morning with a public statement. WHERE: OpenAI's San Francisco headquarters, with the resignation letter published on their official news channel. WHY: The researcher expressed frustration with what they describe as deprioritization of alignment research—the critical work of ensuring AI systems behave according to human values. They cited pressure to accelerate deployment timelines over thorough safety validation. HOW: The departure came as a public statement, not a quiet resignation, with the researcher urging others in the AI safety community to 'speak up' and advocate for safety-first development practices. PREVIOUSLY: OpenAI had previously positioned itself as prioritizing safety research, especially following the release of GPT-5. The organization made public commitments to alignment work and Constitutional AI principles. Now: This resignation signals a significant shift—departing researchers claim those commitments have been deprioritized in favor of faster model deployment. This represents a fundamental tension in AI development: moving quickly to capture market opportunity versus moving carefully to ensure safety and alignment. The departure is notable because safety researchers are in high demand, making their departure a signal that the culture or priorities have genuinely shifted.",
        "why": "How companies handle AI safety concerns internally shapes public trust and regulatory response. When senior researchers depart citing safety concerns, it signals potential cracks in organizational values. This matters because it may influence regulatory scrutiny, talent retention across the industry, and public perception of AI development priorities.",
        "signal": "Culture beats process. Who leaves an organization reveals what it values.",
        "source": "OpenAI · TechCrunch",
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
        "scale": "WHO: NVIDIA, the semiconductor giant, in partnership with CoreWeave, a specialized AI infrastructure provider. WHAT: DGX Spark 64GB—a compact 4-GPU system specifically optimized for running open-weights large language models like Llama and Mistral with sub-20ms latency. This brings enterprise-grade inference to on-premises deployments. WHEN: Announced today with shipping beginning October 15, 2026. WHERE: Designed for on-premises, air-gapped data centers where organizations need full control and can't rely on cloud providers. WHY: Enterprises face two key problems with current AI inference: (1) Cloud API latency exceeds 200ms, making real-time applications difficult, and (2) per-token costs accumulate quickly at scale. DGX Spark addresses both by moving inference to the edge. HOW: Organizations plug in the system, deploy models via NVIDIA NIM (container runtime), and run inference with 10x lower latency and dramatically reduced costs. The system supports multi-LoRA (Low-Rank Adaptation) for specialized agent workloads. PREVIOUSLY: Organizations either ran inference in the cloud (slow, expensive) or built custom servers (complex, error-prone, requiring deep infrastructure expertise). SHIFT: DGX Spark provides a turnkey solution—a pre-built, pre-configured system ready for agentic AI workloads. This changes the economic equation for AI deployment, favoring decentralized, local-first architectures over cloud-dependent models.",
        "why": "Cost-effective local inference opens new use cases in enterprise and edge scenarios. It reduces dependency on cloud providers, improves latency for real-time AI agents, and enables organizations to keep sensitive data on-premises while still accessing powerful AI capabilities.",
        "signal": "The margin between edge and cloud computing is collapsing.",
        "source": "NVIDIA · Enterprise Weekly",
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
        "scale": "WHO: Apple, implementing policy changes via macOS Sonoma 15.1. Triggered by: Meta's Muse AI agent, which users reported recording desktop activity without explicit consent. WHAT: macOS now restricts Full Disk Access (FDA)—a powerful permission that allows apps to read all user files. Only Apple's own system apps and properly sandboxed third-party apps can access Full Disk Access. Meta Muse is now blocked from this capability. WHEN: Available now in macOS 15.1. WHERE: macOS Sonoma and future releases. WHY: Users discovered Meta Muse was recording screen content without clear consent mechanisms, raising privacy alarms. This incident exposed that a high-profile developer was using powerful OS-level permissions for capabilities users hadn't explicitly authorized. HOW: Apple tightened the technical gates, reducing which apps can request Full Disk Access and requiring stricter sandboxing for third-party apps. PREVIOUSLY: Full Disk Access was available to developers building productivity tools and system utilities, with minimal guardrails. SHIFT: Privacy concerns now drive OS-level policy. This marks a turning point where AI agent capabilities are directly triggering OS security tightening. Platform gatekeeping on AI tools is now explicit and enforceable at the OS level.",
        "why": "Trust in AI tools depends on transparent data handling and user control. As AI agents become more capable and autonomous, OS-level restrictions establish clear guardrails. This shapes how AI tools can operate in the future—more transparent, with explicit user consent.",
        "signal": "Privacy is becoming a platform policy, not a feature request.",
        "source": "Apple · TechCrunch",
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
        "scale": "WHO: Anthropic (Claude), OpenAI (ChatGPT), Google (Gemini), Meta (Llama agents), and others. WHAT: SMS-based agent access launched simultaneously across multiple providers. Users text a number, type a prompt, and receive AI-generated responses—no app download required. Capabilities include planning, research, code generation, and task automation via text. WHEN: Rolled out September 28 – October 2, 2026. Claude SMS reached 5M users in 48 hours. WHERE: Global SMS access with local numbers in 40+ countries. US: +1-415-CLAUDE-1. Works on any phone with SMS capability—feature phones, smartphones, burners. WHY: SMS reaches 2 billion people without requiring app downloads or store reviews. It bypasses app-store friction entirely and works on devices that can't run modern apps. This expands the addressable market from 1.5B app users to 2B SMS users—a 33% market expansion. HOW: Users text prompts to AI agents, which respond with summaries, itineraries, code snippets, or research. For complex tasks, escalation to web or SMS clarifications. PREVIOUSLY: AI agents required websites or dedicated apps—barriers to entry for feature-phone users and markets with poor app-store infrastructure. SHIFT: Distribution now trumps capability. The best AI is the one you already have open (your SMS app). This move targets emerging markets and users with older devices, fundamentally democratizing access to AI agents.",
        "why": "Friction drops when AI lives where people already spend time. SMS is the only universal communication channel across all phones and markets. This could accelerate global AI adoption, especially in markets where smartphone penetration is lower.",
        "signal": "Distribution wins over capability. The best AI is the one you already have open.",
        "source": "TechCrunch · App Intelligence",
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
        "scale": "WHO: Meta, as part of broader AR/wearables strategy. WHAT: Discontinuing Muse desktop app (abandoned after privacy backlash). Launching 'Muse Glass' beta on Ray-Ban smart glasses—on-device AI agents with no screen recording. WHEN: Muse Glass available to Ray-Ban beta users starting October 5, 2026. WHERE: Shifting from desktop/Mac to physical wearables. WHY: Desktop Muse faced severe privacy backlash for full-screen recording without explicit per-use consent. Public and regulatory pressure made the desktop product untenable. AR glasses offer a different trust model—what the camera sees is what users see, creating optical alignment between surveillance and utility. HOW: On-device processing runs AI agents directly on Ray-Ban hardware. Camera input is limited to what's physically in the user's field of view (not the entire desktop). Users control when the camera records. PREVIOUSLY: Muse on desktop was positioned as a productivity tool, similar to Copilot Recall (Microsoft's competitor product). Desktop screen recording was framed as 'always-on observation' for better AI assistance. SHIFT: The form factor shapes the trust contract. AR glasses create natural boundaries—camera sees what user sees. This sidesteps the 'surveillance of your entire desktop' concern. Meta is betting that surveillance anxiety is solved by physical framing, not just permission dialogs. This represents a fundamental insight: where AI observes (eye level vs. desktop) and what users perceive (shared field of view vs. background monitoring) matters as much as the capability itself.",
        "why": "Where AI observes matters as much as what it observes. AR glasses create a visible, physical boundary between observation and privacy. This could be a template for building trust in AI surveillance: make it visible, make it limited, make it aligned with user perspective.",
        "signal": "The form factor shapes the trust contract.",
        "source": "Meta · TechCrunch",
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

print(f"[EDITOR] Selected {len(stories)} stories for today's edition.")

# Load and rotate Word of the Day with deduplication
print("[EDITOR] Loading Word of the Day list...")
try:
    with open("words_of_day.json", "r") as f:
        words_list = json.load(f)

    today = str(date.today())
    # Find a word that wasn't used today
    word = None
    for w in words_list:
        if w.get("last_used") != today:
            word = w
            w["last_used"] = today
            break

    # If all words used today, pick the oldest (shouldn't happen daily)
    if not word:
        word = min(words_list, key=lambda w: w.get("last_used") or "2000-01-01")
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

# Load newsletter template
print("[EDITOR] Loading newsletter template...")
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

# Inject data into template
html = html.replace("%STORIES%", json.dumps(stories_for_template))
html = html.replace("%WORD%", json.dumps(word_for_template))

# Old HTML template code (kept for reference, not used):
html_old = """<!DOCTYPE html>
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

    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>
        // Initialize Supabase (using your public credentials)
        const SUPABASE_URL = 'https://mzsipmeuthconogugwry.supabase.co';
        const SUPABASE_KEY = 'sb_publishable_AHLzBSVlyyQJSKIZFD2Nyg_R2WHJfMG';
        let supabase = null;
        function getSupabase() {
            if (!supabase && window.supabase) {
                supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
            }
            return supabase;
        }

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
                    <div class="story ${idx === 0 ? 'expanded' : ''}" data-id="${story.id}">
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
                                <button class="vote-btn" onclick="voteStory('${story.id}', 'up', this)">👍 More like this</button>
                                <button class="vote-btn" onclick="voteStory('${story.id}', 'down', this)">👎 Less</button>
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

        // Vote handler - Send to Supabase
        async function voteStory(storyId, type, buttonElement) {
            // Find the story object by ID
            const story = STORIES.find(s => s.id === storyId);
            if (!story) {
                console.error('Story not found:', storyId);
                return;
            }

            // Use provided button element
            const button = buttonElement;

            try {
                // Generate session ID if not exists
                let sessionId = localStorage.getItem('morning-prompt-session');
                if (!sessionId) {
                    sessionId = 'user-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
                    localStorage.setItem('morning-prompt-session', sessionId);
                }

                // Show loading state
                button.disabled = true;
                button.style.opacity = '0.6';
                button.textContent = 'Saving...';

                // Get story ID from database
                const sb = getSupabase();
                if (!sb) throw new Error('Supabase not loaded');

                const { data: stories, error: searchError } = await sb
                    .from('stories')
                    .select('id')
                    .eq('story_id', storyId)
                    .limit(1);

                if (searchError || !stories || stories.length === 0) {
                    throw new Error('Story not found in database');
                }

                const dbStoryId = stories[0].id;

                // Send vote to Supabase
                const { data, error } = await sb
                    .from('votes')
                    .insert({
                        story_id: dbStoryId,
                        vote_type: type,
                        user_id: sessionId
                    });

                if (error) {
                    throw error;
                }

                // Visual feedback - success
                button.textContent = type === 'up' ? '👍 Voted!' : '👎 Noted!';
                button.style.background = '#4db87a';
                button.style.color = '#faf6eb';

                console.log(`Vote saved to Supabase: ${type} on "${story.head}"`);

                // Re-enable after 2 seconds
                setTimeout(() => {
                    button.disabled = false;
                    button.style.opacity = '1';
                    button.textContent = type === 'up' ? '👍 More like this' : '👎 Less';
                    button.style.background = 'transparent';
                    button.style.color = '#1a1710';
                }, 2000);

            } catch (error) {
                console.error('Error recording vote:', error);
                button.textContent = 'Failed';
                button.style.background = '#b33425';

                // Reset after 3 seconds
                setTimeout(() => {
                    button.disabled = false;
                    button.style.opacity = '1';
                    button.textContent = type === 'up' ? '👍 More like this' : '👎 Less';
                    button.style.background = 'transparent';
                    button.style.color = '#1a1710';
                }, 3000);
            }
        }

        // Call directly - inline script runs after DOM is ready
        renderStories();
        renderWord();
    </script>
</body>
</html>
"""

# Write to output (use newsletter-final.html as the destination)
output_file = "output/newsletter-final.html"
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

# Update published.json to avoid re-publishing same stories
try:
    published_file = "published.json"
    published = []
    if os.path.exists(published_file):
        with open(published_file, "r") as f:
            published = json.load(f)

    # Add today's stories to published list
    for story in stories:
        published.append({
            "url": story.get("links", [[None, ""]])[0][1] if story.get("links") else "",
            "headline": story["head"],
            "date": str(date.today())
        })

    with open(published_file, "w") as f:
        json.dump(published, f, indent=2)

    print(f"[EDITOR] Updated published.json with {len(stories)} stories")
except Exception as e:
    print(f"[WARN] Failed to update published.json: {e}")
