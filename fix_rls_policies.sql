-- Fix missing RLS INSERT policies for editions table
-- Run this in Supabase SQL Editor

-- Add INSERT policy for editions (needed for GitHub Actions to create new editions)
CREATE POLICY "enable_insert_editions" ON editions FOR INSERT WITH CHECK (true);

-- Add UPDATE policy for editions (needed for updating published_at timestamp)
CREATE POLICY "enable_update_editions" ON editions FOR UPDATE USING (true) WITH CHECK (true);

-- Verify stories INSERT policy exists (should already be there, but adding for completeness)
CREATE POLICY "enable_insert_stories" ON stories FOR INSERT WITH CHECK (true);

-- Verify stories UPDATE policy exists
CREATE POLICY "enable_update_stories" ON stories FOR UPDATE USING (true) WITH CHECK (true);

-- Verify user_preferences INSERT policy exists
CREATE POLICY "enable_insert_user_prefs" ON user_preferences FOR INSERT WITH CHECK (true);
CREATE POLICY "enable_update_user_prefs" ON user_preferences FOR UPDATE USING (true) WITH CHECK (true);
