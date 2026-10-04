-- Fix Supabase schema constraints
-- Run this in Supabase SQL Editor

-- 1. FIX: Allow same URL in different editions (daily rotation)
-- Drop old UNIQUE constraint that prevents re-publishing same URL
ALTER TABLE stories DROP CONSTRAINT IF EXISTS stories_source_url_key;

-- Add new constraint: same URL only once per edition, not globally
ALTER TABLE stories ADD UNIQUE(edition_id, source_url);

-- 2. FIX: Add missing RLS INSERT policies for GitHub Actions
CREATE POLICY IF NOT EXISTS "enable_insert_editions" ON editions FOR INSERT WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "enable_update_editions" ON editions FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "enable_insert_stories" ON stories FOR INSERT WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "enable_update_stories" ON stories FOR UPDATE USING (true) WITH CHECK (true);

-- 3. VERIFY: Check current schema
SELECT table_name, constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name IN ('stories', 'editions')
ORDER BY table_name;
