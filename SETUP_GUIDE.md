# The Morning Prompt — Setup Guide

Follow these steps to go from code to production.

---

## Phase 1: Local Testing (5 minutes)

### 1.1 Install Dependencies
```bash
cd "C:\Users\jaina\OneDrive\Desktop\PM\What's new in AI"
pip install -r requirements.txt
```

### 1.2 Test the Fetcher
```bash
python fetch.py
```
Expected output: 25 ranked news candidates. ✓

### 1.3 Test the Editor
```bash
python editor.py
```
Expected output: `output/2026-10-03.html` generated. ✓

### 1.4 View the Edition
Open `output/2026-10-03.html` in your browser. Should see:
- 5 stories in collapsible cards (lead story expanded)
- Word of the Day sidebar
- Vote buttons inside each story
- Mobile-friendly layout

---

## Phase 2: Supabase Setup (10 minutes)

### 2.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up (free tier is enough)
3. Create a new project:
   - **Name:** The-Morning-Prompt
   - **Region:** Choose closest to you (India? Singapore?)
   - **Password:** Generate secure password, save it
4. Wait for project to be created (~2 minutes)

### 2.2 Get API Keys

1. Go to **Settings → API**
2. Copy:
   - `Project URL` → Paste as `SUPABASE_URL` in `.env`
   - `anon public` key → Paste as `SUPABASE_KEY` in `.env`

Example:
```
SUPABASE_URL=https://abcdefgh.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2.3 Create Database Schema

1. In Supabase, go to **SQL Editor** (left sidebar)
2. Create new query
3. Open `schema.sql` from the repo
4. Copy all contents → Paste into Supabase SQL Editor
5. Click **Run** (play button)
6. Should see: "Success. Rows affected: 0" (tables created)

### 2.4 Create .env File (Local)

```bash
# Copy template
cp .env.example .env

# Edit .env and add your Supabase credentials
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key
```

### 2.5 Test Supabase Connection

```bash
python -c "from supabase_client import get_supabase_client; client = get_supabase_client(); print('Connected!' if client.enabled else 'Not connected')"
```

Should print: `Connected!` ✓

---

## Phase 3: Push to GitHub (3 minutes)

### 3.1 Create .env in .gitignore (Already Done)

The `.gitignore` already includes `.env` so your credentials won't be pushed.

### 3.2 Push to GitHub

```bash
git push -u origin main
```

(First push may ask for credentials)

### 3.3 Verify on GitHub

Go to [https://github.com/jainam-pm/The-AI-Newsletter](https://github.com/jainam-pm/The-AI-Newsletter)

Should see all files:
- ✓ .claude/skills/morning-prompt/SKILL.md
- ✓ fetch.py
- ✓ editor.py
- ✓ supabase_client.py
- ✓ schema.sql
- ✓ template.html
- ✓ glossary.yaml
- ✓ README.md
- ✓ .gitignore
- ✓ requirements.txt

---

## Phase 4: Schedule Daily Run (2 minutes)

Now that Supabase is set up, the daily routine will auto-save to the database.

### Option A: Cloud Routine (Recommended)

Run this in Claude Code:
```
/schedule daily at 8:30 am IST run the morning-prompt skill
```

**Benefits:**
- ✅ Runs in cloud (laptop can be closed)
- ✅ Auto-commits to GitHub
- ✅ Auto-saves to Supabase
- ✅ Reliable scheduling

### Option B: Desktop Routine (Local)

1. Open Claude Code Desktop
2. Go to **Routines** (top-right menu)
3. Click **New Routine**
4. Set:
   - Name: "Morning Prompt"
   - Frequency: Daily
   - Time: 8:30 AM
   - Action: Run `/morning-prompt` skill
5. Save

**Limitations:**
- Requires laptop to be running at 8:30 AM
- Only runs if Claude Code is open

---

## Phase 5: Email Delivery (Optional)

### 5.1 Enable Gmail Integration

Set these in `.env`:
```bash
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

### 5.2 Get Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security (left sidebar)
3. App passwords (requires 2FA enabled)
4. Select: Mail, Windows Computer
5. Copy 16-character password → Paste into `.env`

### 5.3 Update editor.py

Add email sending after rendering HTML:
```python
if os.getenv("GMAIL_USER"):
    send_edition_email(output_file)
```

(Implementation: Use `smtplib` to send HTML email)

---

## Phase 6: Monitor & Iterate

### Check Today's Edition

**In GitHub:**
- Go to [https://github.com/jainam-pm/The-AI-Newsletter/tree/main/output](https://github.com/jainam-pm/The-AI-Newsletter/tree/main/output)
- Should see `2026-10-03.html`, `2026-10-04.html`, etc. daily

**In Supabase:**
1. Go to **Table Editor**
2. Click **editions** → See all published dates
3. Click **stories** → See all stories with votes
4. Click **votes** → See which stories got 👍 vs 👎

### Customize

- **Add sources:** Edit `sources.yaml`, add more RSS feeds
- **Adjust scoring:** Edit `fetch.py` `score_story()` function
- **Change colors:** Edit `template.html` `CATS` object
- **Change time:** `/schedule ... <new time>` in Claude Code

### Use Votes for Personalization (v2)

```python
# In fetch.py, after scoring:
votes = supabase.get_votes_for_story(story_id)
if votes["up"] > votes["down"]:
    score += 1  # Boost stories users liked
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Supabase not configured" | Check `.env` has `SUPABASE_URL` and `SUPABASE_KEY` |
| "ModuleNotFoundError: supabase" | Run `pip install supabase` |
| Fetch returns 0 stories | Check internet, verify `sources.yaml` URLs work |
| Routine didn't run at 8:30 AM | Cloud routines need GitHub repo set up. Desktop routines need Claude Code open. |
| HTML won't render | Check browser console (F12) for JS errors. Make sure story data is valid JSON. |
| Can't push to GitHub | Authenticate: `git config --global user.email` and `git config --global user.name` |

---

## What's Next?

### Short-term (This week)
1. ✅ Set up Supabase
2. ✅ Push to GitHub
3. ✅ Schedule daily run
4. ⬜ Monitor first 3 editions
5. ⬜ Tweak sources if needed

### Medium-term (This month)
- ⬜ Add email delivery
- ⬜ Create web dashboard to view past editions
- ⬜ Add user feedback form
- ⬜ Set up voting analytics

### Long-term (Next quarter)
- ⬜ Vote-driven personalization
- ⬜ Weekly digest / monthly summary
- ⬜ Trending topics across editions
- ⬜ Open-source & tools section

---

## Need Help?

- **GitHub Issues:** [Open an issue](https://github.com/jainam-pm/The-AI-Newsletter/issues)
- **Claude Code:** Type `/help` for CLI tips
- **Supabase Docs:** [supabase.com/docs](https://supabase.com/docs)

---

**You're all set! 🚀**

Your Morning Prompt will be live at 8:30 AM IST every day.

Next step: Run `/schedule daily at 8:30 am IST run the morning-prompt skill` in Claude Code.
