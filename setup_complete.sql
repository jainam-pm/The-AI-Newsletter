-- The Morning Prompt - Complete Supabase Setup
-- Copy ALL of this into your Supabase SQL Editor and run

-- ============================================
-- 1. GRANT PERMISSIONS TO ANON USER
-- ============================================

GRANT SELECT, INSERT, UPDATE, DELETE ON public.editions TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.stories TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.votes TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_preferences TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.reading_history TO anon;

-- Grant sequence permissions (for auto-increment IDs)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;

-- ============================================
-- 2. DISABLE RLS (Row Level Security)
-- ============================================
-- For development/testing, we disable RLS
-- In production, you'd set up proper RLS policies

ALTER TABLE editions DISABLE ROW LEVEL SECURITY;
ALTER TABLE stories DISABLE ROW LEVEL SECURITY;
ALTER TABLE votes DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences DISABLE ROW LEVEL SECURITY;
ALTER TABLE reading_history DISABLE ROW LEVEL SECURITY;

-- ============================================
-- 3. VERIFY SETUP
-- ============================================
-- Run these queries to verify everything works:

-- Check 1: Can we insert into editions?
-- INSERT INTO editions (date, headline, description) VALUES ('2026-01-01'::date, 'Test', 'Test edition');

-- Check 2: Can we query editions?
-- SELECT COUNT(*) FROM editions;

-- Check 3: Can we see tables?
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- ============================================
-- DONE! Your Supabase is now ready.
-- ============================================
