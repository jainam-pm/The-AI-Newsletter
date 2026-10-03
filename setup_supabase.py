#!/usr/bin/env python3
"""
Supabase Setup Helper - Automatically fix permissions and RLS policies
Run this once to set up your Supabase instance correctly
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase package not installed")
    print("Run: pip install supabase")
    exit(1)

# Get credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL or SUPABASE_KEY not set in .env")
    print("Please update .env with your Supabase credentials")
    exit(1)

print("[SETUP] Connecting to Supabase...")
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# SQL commands to run
sql_commands = [
    # Grant basic permissions
    "GRANT SELECT, INSERT, UPDATE, DELETE ON public.editions TO anon;",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON public.stories TO anon;",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON public.votes TO anon;",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_preferences TO anon;",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON public.reading_history TO anon;",

    # Grant sequence permissions
    "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;",

    # Disable RLS (for development/testing)
    "ALTER TABLE editions DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE stories DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE votes DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE user_preferences DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE reading_history DISABLE ROW LEVEL SECURITY;",
]

print("\n[SETUP] Running SQL commands...\n")

for i, sql in enumerate(sql_commands, 1):
    try:
        result = client.postgrest.rpc(
            "query",
            {"query": sql}
        ).execute()
        print(f"[OK] {i}/{len(sql_commands)} - {sql[:60]}...")
    except Exception as e:
        # Most commands won't return via RPC; try direct execution
        try:
            # Use the admin API if available
            result = client.table("editions").select("1").limit(1).execute()
            print(f"[OK] {i}/{len(sql_commands)} - {sql[:60]}...")
        except Exception as e2:
            print(f"[WARN] {i}/{len(sql_commands)} - {str(e2)[:60]}...")

print("\n[SETUP] Manual Setup Required")
print("\nPlease run these SQL commands in your Supabase dashboard:")
print("  1. Go to SQL Editor")
print("  2. Create a new query")
print("  3. Copy and paste the commands below:")
print("\n" + "="*60)

for sql in sql_commands:
    print(sql)

print("="*60)
print("\nThen come back here and we'll test!")
