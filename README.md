# The Morning Prompt — Daily AI Newsletter

A production-ready AI news aggregator that delivers the top 5 AI stories every morning at 8:30 AM IST, complete with competitive analysis, votes, and personalization.

**Status:** Live ✅  
**First Edition:** October 3, 2026  
**Cost:** ~$1/month (Haiku 4.5 + Supabase free tier)  
**Delivery:** Cloud Routine (no laptop required)

---

## What You Get

📰 **Daily Newspaper**
- 5 curated AI stories (handpicked from 25+ candidates)
- 5W1H coverage (Who, What, When, Where, Why, How)
- Competitive analysis (what competitors are doing)
- Before → Now comparison
- Source links + vote buttons (👍/👎)

🧠 **Word of the Day**
- Technical term from today's stories
- Definition + why it matters
- Tied to relevant story

📊 **User Data**
- Vote tracking (personalize future editions)
- Reading history (expand rate, time spent)
- User preferences (favorite categories, companies)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Daily @ 8:30 AM IST (Claude Code Routine)          │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   fetch.py               SKILL.md (Claude)
   (Python)               (Editor prompt)
   - Pull 35+ RSS/APIs    - Pick 5 stories
   - Score 25 candidates  - Fetch full articles
   - Deduplicate          - Write summaries
   - ~0 LLM tokens        - Render HTML
                          - Save to Supabase
        │                         │
        └────────────┬────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Supabase (DB)   │
            ├─────────────────┤
            │ • editions      │
            │ • stories       │
            │ • votes         │
            │ • reading_hist  │
            │ • user_prefs    │
            └─────────────────┘
                     │
                     ▼
         HTML Edition + Email Delivery
```

---

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/jainam-pm/The-AI-Newsletter.git
cd The-AI-Newsletter
python -m pip install -r requirements.txt
```

### 2. Create .env File

```bash
cp .env.example .env
```

Fill in your Supabase credentials:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 3. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) → Create free project
2. Go to SQL Editor → Paste `schema.sql` → Run
3. Get your API URL & anon key from Settings → API
4. Add to `.env`

### 4. Test Locally

```bash
# Fetch candidates
python fetch.py

# Generate edition (manual test)
python editor.py

# Check output/YYYY-MM-DD.html in your browser
```

### 5. Schedule Daily Run

**Option A: Cloud Routine (Recommended)**
```
/schedule daily at 8:30 am IST run the morning-prompt skill
```

**Option B: Desktop (Local)**
- Claude Code Desktop → Routines → New → Local → Daily at 8:30 AM

---

## How It Works

### Step 1: Fetch Candidates (fetch.py)
- Hits 35+ RSS feeds + APIs (zero LLM tokens)
- Pulls last 24 hours of stories
- Deduplicates by URL + fuzzy title match
- Scores by: multi-source coverage, official announcements, viral posts
- Outputs ~25 ranked candidates

### Step 2: Editorial Pick (SKILL.md)
- Claude reads 25 candidates
- Selects 5 most significant
- Fetches full articles (capped at 1,500 words each)
- Writes 5W1H for each
- Competitive analysis (1 web search per story)
- Picks Word of the Day

### Step 3: Store & Deliver
- Renders HTML newspaper
- Saves to `output/YYYY-MM-DD.html`
- Stores in Supabase (stories, votes, metadata)
- Optional: Sends email with link

---

## Database Schema

### editions
Daily edition metadata
```
| id | date | headline | description | published_at |
```

### stories
Individual stories within edition
```
| id | edition_id | headline | deck | category | source_url | companies | full_content (JSONB) |
```

### votes
User feedback (👍/👎)
```
| id | story_id | user_id | vote_type | created_at |
```

### words_of_day
Historical words (avoid repeats)
```
| id | edition_id | term | definition | why_matters |
```

### user_preferences
Personalization (future feature)
```
| user_id | preferred_categories | exclude_categories | preferred_companies |
```

### reading_history
Track engagement
```
| id | user_id | story_id | expanded | time_spent_seconds |
```

---

## Token Budget

| Step | Tokens | Cost |
|------|--------|------|
| Fetch 35 feeds | 0 (Python) | $0 |
| Score 25 → pick 5 | 0 (Python) | $0 |
| Candidates to Claude | ~2,500 in | $0.0025 |
| Skill instructions | ~1,500 in | $0.0015 |
| Fetch 5 articles | ~6,000 in | $0.006 |
| Write + render | ~4,000 out | $0.02 |
| **TOTAL/DAY** | **~13.5K in/out** | **~$0.035** |
| **MONTHLY** | | **~$1.05** |

Using Haiku 4.5 on a Claude Code Pro/Max plan (usage counts to your subscription).

---

## Features (v1)

✅ Multi-source aggregation (30+ feeds)  
✅ Intelligent scoring & deduplication  
✅ Follow-up detection (updates to prior stories)  
✅ Full article fetching + summarization  
✅ Competitive analysis per story  
✅ Editorial newspaper design (light theme)  
✅ Mobile responsive  
✅ Vote tracking (Supabase)  
✅ Daily scheduling (Claude Code Routine)  
✅ Version control (Git)  

---

## Future Features (v2)

- [ ] Vote-driven personalization (boost liked categories)
- [ ] Email delivery (Gmail API)
- [ ] Web interface to read editions
- [ ] User dashboard (voting history, preferences)
- [ ] Trending topics across editions
- [ ] Weekly digest / monthly summary
- [ ] AI-powered recommendations ("You loved security stories, here's 3 more")
- [ ] Trending repos + open-source section
- [ ] Skill Shelf (new AI skills/tools each day)

---

## Configuration

### sources.yaml
Add/remove RSS feeds and API sources. Format:
```yaml
- name: "Source Name"
  url: "https://..."
  type: "rss"  # or "api", "scrape"
  category: "AI Labs"
```

### glossary.yaml
~150 AI/tech terms for Word of the Day. After using a term, set `used: true`.

### fetch.py Scoring
Adjust weights in `score_story()`:
```python
if source_count >= 3:
    score += 3  # Multi-source boost
if story.get("source") in ["openai", "google_ai", ...]:
    score += 2  # Official announcement boost
```

### template.html
Edit colors in CATS object:
```javascript
const CATS = {
  models:   { label: "Models",    color: "#2a6fa8" },
  security: { label: "Security",  color: "#b33425" },
  // ...
};
```

---

## Development

### Run the Full Pipeline
```bash
# 1. Fetch candidates
python fetch.py

# 2. Generate edition (simulated Claude)
python editor.py

# 3. View output
open output/2026-10-03.html
```

### Test Supabase Connection
```bash
python -c "from supabase_client import get_supabase_client; client = get_supabase_client(); print(client.enabled)"
```

### View Logs
```bash
# Check recent editions
tail -20 output/$(date +%Y-%m-%d).html

# Check vote counts
# (Via Supabase dashboard)
```

---

## Deployment

### GitHub
```bash
git add .
git commit -m "Update: [description]"
git push origin main
```

### Supabase
- Migrations are in `schema.sql`
- Row-level security (RLS) is enabled
- Free tier supports ~500K rows (enough for 3+ years of daily editions)

### Email Delivery (Optional)
Set `GMAIL_APP_PASSWORD` in `.env` to enable email digests.
(Requires Gmail 2FA + app password)

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'feedparser'"**
```bash
pip install -r requirements.txt
```

**"Supabase not configured"**
- Check `.env` has `SUPABASE_URL` and `SUPABASE_KEY`
- Votes/preferences won't be stored but edition still works

**"Fetch returned 0 stories"**
- Check `sources.yaml` URLs are valid
- Run manually: `python fetch.py 2>&1 | head -30`
- Some feeds may be down; check status

**"Editor script times out"**
- Might be fetching articles slowly
- Increase timeout or disable full-article fetch for testing

---

## Support

- **Questions:** Open an issue on GitHub
- **Contributions:** PRs welcome
- **Feature requests:** Discussions tab

---

## License

MIT — Use freely, fork, modify, distribute.

---

**Made with ❤️ and Claude Code**

Next edition: Tomorrow at 8:30 AM IST 📰
