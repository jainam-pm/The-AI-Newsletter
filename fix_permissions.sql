-- Grant permissions to anon role for The Morning Prompt tables

-- Grant SELECT/INSERT/UPDATE permissions on all tables
GRANT SELECT, INSERT, UPDATE ON public.editions TO anon;
GRANT SELECT, INSERT, UPDATE ON public.stories TO anon;
GRANT SELECT, INSERT, UPDATE ON public.votes TO anon;
GRANT SELECT, INSERT, UPDATE ON public.user_preferences TO anon;
GRANT SELECT, INSERT, UPDATE ON public.reading_history TO anon;

-- Grant sequence permissions (needed for auto-increment IDs)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;
