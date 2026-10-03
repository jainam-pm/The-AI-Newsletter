-- The Morning Prompt — Supabase Schema
-- Run this in your Supabase SQL editor

-- Table: editions
-- Stores each daily edition metadata
CREATE TABLE IF NOT EXISTS editions (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL UNIQUE,
  headline TEXT NOT NULL,
  description TEXT,
  fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  published_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: stories
-- Individual stories within each edition
CREATE TABLE IF NOT EXISTS stories (
  id BIGSERIAL PRIMARY KEY,
  edition_id BIGINT NOT NULL REFERENCES editions(id) ON DELETE CASCADE,
  story_id TEXT NOT NULL, -- s1, s2, s3, etc.
  headline TEXT NOT NULL,
  deck TEXT NOT NULL,
  category TEXT NOT NULL, -- models, security, privacy, builders, policy, research, india
  source_url TEXT NOT NULL UNIQUE,
  source_name TEXT,
  companies TEXT[], -- Array of companies mentioned
  summary TEXT,
  full_content JSONB, -- 5W1H rows, competitive analysis, etc.
  position INT, -- 1-5 for display order
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: votes
-- User votes on stories (👍/👎)
CREATE TABLE IF NOT EXISTS votes (
  id BIGSERIAL PRIMARY KEY,
  story_id BIGINT NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
  user_id TEXT, -- Null = anonymous, or session ID
  vote_type TEXT NOT NULL CHECK (vote_type IN ('up', 'down')), -- up = 👍, down = 👎
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: user_preferences
-- Store user personalization data
CREATE TABLE IF NOT EXISTS user_preferences (
  id BIGSERIAL PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE, -- Session ID or email
  preferred_categories TEXT[], -- e.g., ['models', 'builders']
  exclude_categories TEXT[],
  preferred_companies TEXT[], -- e.g., ['Anthropic', 'OpenAI']
  prefer_depth TEXT DEFAULT 'balanced', -- quick, balanced, deep
  email_delivery BOOLEAN DEFAULT false,
  email_address TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: words_of_day
-- Word of the Day history (avoid repeats)
CREATE TABLE IF NOT EXISTS words_of_day (
  id BIGSERIAL PRIMARY KEY,
  edition_id BIGINT NOT NULL REFERENCES editions(id) ON DELETE CASCADE,
  term TEXT NOT NULL,
  pos TEXT, -- part of speech
  definition TEXT NOT NULL,
  why_matters TEXT,
  tied_story_id BIGINT REFERENCES stories(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: reading_history
-- Track what users have read (for future recommendations)
CREATE TABLE IF NOT EXISTS reading_history (
  id BIGSERIAL PRIMARY KEY,
  user_id TEXT, -- Anonymous session ID
  story_id BIGINT NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
  read_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  time_spent_seconds INT, -- How long they spent reading
  expanded BOOLEAN DEFAULT false -- Did they click to expand?
);

-- Indexes for performance
CREATE INDEX idx_editions_date ON editions(date DESC);
CREATE INDEX idx_stories_edition ON stories(edition_id);
CREATE INDEX idx_stories_category ON stories(category);
CREATE INDEX idx_votes_story ON votes(story_id);
CREATE INDEX idx_votes_user ON votes(user_id);
CREATE INDEX idx_user_prefs_user ON user_preferences(user_id);
CREATE INDEX idx_reading_user ON reading_history(user_id);
CREATE INDEX idx_reading_story ON reading_history(story_id);

-- Enable Row Level Security (RLS) for privacy
ALTER TABLE editions ENABLE ROW LEVEL SECURITY;
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE reading_history ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Anyone can read editions/stories
CREATE POLICY "enable_read_editions" ON editions FOR SELECT USING (true);
CREATE POLICY "enable_read_stories" ON stories FOR SELECT USING (true);

-- RLS Policy: Anonymous votes (identified by session ID)
CREATE POLICY "enable_insert_votes" ON votes FOR INSERT WITH CHECK (true);
CREATE POLICY "enable_read_votes" ON votes FOR SELECT USING (true);

-- RLS Policy: User can see their own preferences
CREATE POLICY "enable_user_prefs" ON user_preferences FOR ALL USING (true);

-- RLS Policy: User can log their own reading history
CREATE POLICY "enable_reading_history" ON reading_history FOR INSERT WITH CHECK (true);
CREATE POLICY "enable_read_reading_history" ON reading_history FOR SELECT USING (true);
