# The Morning Prompt — Production Deployment Guide

## Overview
This system deploys to **Vercel** for hosting + **GitHub Actions** for daily 12 PM newsletter generation.

## Architecture
- **Scheduler**: GitHub Actions (runs daily at 12 PM UTC)
- **Newsletter Generator**: Python (`editor.py`)
- **Data Storage**: Supabase PostgreSQL (stories, votes, word rotation state)
- **Frontend**: Vercel-hosted HTML + JavaScript
- **Output**: `output/newsletter-final.html` (auto-generated, version-controlled)

## Step 1: Push to GitHub

```bash
cd "C:\Users\jaina\OneDrive\Desktop\PM\What's new in AI"
git add .
git commit -m "Add production deployment configuration

- Add vercel.json for Vercel hosting
- Add GitHub Actions workflow for daily 12 PM generation
- Add package.json for Node.js dependencies

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
git push origin main
```

**Note**: If repo doesn't exist on GitHub yet:
1. Create repo at github.com/new
2. Copy repo URL
3. Run: `git remote add origin <URL>` then `git push -u origin main`

## Step 2: Configure GitHub Secrets

Go to **GitHub Repo → Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `SUPABASE_URL` | Your Supabase project URL (e.g., `https://mzsipmeuthconogugwry.supabase.co`) |
| `SUPABASE_ANON_KEY` | Supabase anonymous public key |

These are used by GitHub Actions to run `editor.py` and save stories to Supabase.

## Step 3: Deploy to Vercel

### Option A: Connect GitHub Repo (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project" → "Import Git Repository"
3. Select your GitHub repo
4. Vercel auto-detects `vercel.json` and `package.json`
5. Add the same Supabase environment variables in Vercel project settings
6. Click "Deploy"

### Option B: CLI Deployment
```bash
npm i -g vercel
vercel login
vercel --prod
```

## Step 4: Verify Deployment

### Test Manual Run
GitHub Actions → Workflows → "Generate Daily Newsletter" → "Run workflow" → Run

### View Results
- Check repo for new commit with generated newsletter
- Visit Vercel deployment URL → `/output/newsletter-final.html`
- Supabase: `stories` table should have today's entries with votes

### Scheduled Run
- Runs automatically every day at **12:00 PM UTC**
- To adjust timezone: Edit `.github/workflows/generate-newsletter.yml` line 10
  - Example for 12 PM IST: `'0 6 * * *'` (12 PM IST = 6:30 AM UTC, use `30 6` for precision)

## Step 5: Monitor Performance

### Check Timing
`editor.py` outputs timing stats:
```
[TIMER] Fetch:      0.62s
[TIMER] Candidates: 0.15s  
[TIMER] Selection:  0.02s
[TIMER] Render:     0.00s
[TIMER] Supabase:   3.03s
[TIMER] Total:      4.62s (with cache)
```

### Check Logs
- **GitHub Actions**: Repo → Actions → Latest run
- **Vercel**: [vercel.com/dashboard](https://vercel.com) → Project → Deployments → Function logs

## Environment Variables

### Vercel Deployment
```
SUPABASE_URL=https://mzsipmeuthconogugwry.supabase.co
SUPABASE_ANON_KEY=<your-public-key>
```

### Local Testing
Create `.env`:
```
SUPABASE_URL=https://mzsipmeuthconogugwry.supabase.co
SUPABASE_ANON_KEY=<your-public-key>
```

Run locally:
```bash
python editor.py
python fetch.py  # Show candidates
```

## Daily Newsletter Flow

```
12:00 PM (UTC) → GitHub Actions Triggers
        ↓
   Python editor.py runs (fetch + rank + render)
        ↓
   Saves to Supabase (stories, votes, word rotation state)
        ↓
   Commits newsletter-final.html to repo
        ↓
   Vercel auto-deploys updated HTML
        ↓
   Newsletter live at vercel-deployment-url/output/newsletter-final.html
        ↓
   Users vote on stories (tracked in Supabase)
```

## Troubleshooting

### Newsletter not generating?
1. Check GitHub Actions logs: Repo → Actions → Latest workflow run
2. Verify Supabase credentials in repo secrets
3. Test locally: `python editor.py`

### Performance slow?
- RSS cache helps: ~0.6s → 0.06s on cache hit
- Supabase parallel writes: 3 workers writing concurrently
- First run: 20+ seconds (cache building)
- Subsequent runs: ~4-5 seconds

### Votes not persisting?
- Check Supabase dashboard → `stories` table
- Verify `SUPABASE_ANON_KEY` has INSERT/UPDATE permissions
- Clear browser localStorage if session ID corrupted

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Add Supabase secrets to GitHub
3. ✅ Deploy to Vercel
4. ✅ Verify first run (manual trigger)
5. ✅ Monitor daily 12 PM runs
6. 📧 Optional: Add email subscription (POST newsletter HTML to SendGrid, Mailchimp, etc.)

## Files Included

- `editor.py` — Main orchestrator (fetch, rank, render, save)
- `fetch.py` — RSS/API aggregation + scoring
- `newsletter-template.html` — Clean template with placeholders
- `output/newsletter-final.html` — Generated daily edition (version-controlled)
- `.github/workflows/generate-newsletter.yml` — GitHub Actions scheduler
- `vercel.json` — Vercel configuration + cron spec
- `package.json` — Node.js dependencies for Vercel
- `.env.example` — Environment variable template

---

**Production Status**: ✅ Ready for daily deployment

Generated: 2026-10-04 @ 4:30 PM IST
