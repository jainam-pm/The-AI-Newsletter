#!/usr/bin/env python3
"""
Supabase client for The Morning Prompt
Handles database operations for stories, votes, and preferences
"""

import os
from datetime import datetime, date
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("[WARN] Supabase not installed. Install with: pip install supabase")

class SupabaseClient:
    def __init__(self):
        self.enabled = SUPABASE_AVAILABLE and os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY")

        if self.enabled:
            self.client: Client = create_client(
                os.getenv("SUPABASE_URL"),
                os.getenv("SUPABASE_KEY")
            )
            print("[INFO] Supabase connected")
        else:
            print("[WARN] Supabase not configured. Votes & preferences won't be stored.")
            self.client = None

    def create_edition(self, date_obj: date, headline: str, description: str) -> Optional[int]:
        """Create a new edition record"""
        if not self.enabled:
            return None

        try:
            response = self.client.table("editions").insert({
                "date": str(date_obj),
                "headline": headline,
                "description": description,
                "published_at": datetime.now().isoformat()
            }).execute()

            edition_id = response.data[0]["id"] if response.data else None
            print(f"[SUPABASE] Created edition {edition_id} for {date_obj}")
            return edition_id
        except Exception as e:
            print(f"[ERROR] Failed to create edition: {e}")
            return None

    def store_story(self, edition_id: int, story_data: Dict) -> Optional[int]:
        """Store a story record"""
        if not self.enabled:
            return None

        try:
            response = self.client.table("stories").insert({
                "edition_id": edition_id,
                "story_id": story_data.get("id"),
                "headline": story_data.get("head"),
                "deck": story_data.get("deck"),
                "category": story_data.get("cat"),
                "source_url": story_data.get("links", [[None, ""][1])[1] if story_data.get("links") else "",
                "source_name": story_data.get("source"),
                "companies": story_data.get("companies", []),
                "summary": story_data.get("summary"),
                "full_content": story_data,
                "position": int(story_data.get("n", 0))
            }).execute()

            story_id = response.data[0]["id"] if response.data else None
            return story_id
        except Exception as e:
            print(f"[ERROR] Failed to store story: {e}")
            return None

    def store_word_of_day(self, edition_id: int, word_data: Dict, tied_story_id: Optional[int] = None) -> bool:
        """Store Word of the Day"""
        if not self.enabled:
            return False

        try:
            self.client.table("words_of_day").insert({
                "edition_id": edition_id,
                "term": word_data.get("term"),
                "pos": word_data.get("pos"),
                "definition": word_data.get("def"),
                "why_matters": word_data.get("why"),
                "tied_story_id": tied_story_id
            }).execute()

            print(f"[SUPABASE] Stored Word of Day: {word_data.get('term')}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to store word of day: {e}")
            return False

    def get_votes_for_story(self, story_id: int) -> Dict[str, int]:
        """Get vote counts for a story"""
        if not self.enabled:
            return {"up": 0, "down": 0}

        try:
            up_votes = self.client.table("votes").select("id").eq("story_id", story_id).eq("vote_type", "up").execute()
            down_votes = self.client.table("votes").select("id").eq("story_id", story_id).eq("vote_type", "down").execute()

            return {
                "up": len(up_votes.data) if up_votes.data else 0,
                "down": len(down_votes.data) if down_votes.data else 0
            }
        except Exception as e:
            print(f"[ERROR] Failed to get votes: {e}")
            return {"up": 0, "down": 0}

    def record_vote(self, story_id: int, vote_type: str, user_id: Optional[str] = None) -> bool:
        """Record a user vote"""
        if not self.enabled:
            return False

        try:
            self.client.table("votes").insert({
                "story_id": story_id,
                "vote_type": vote_type,
                "user_id": user_id
            }).execute()

            print(f"[SUPABASE] Recorded {vote_type} vote for story {story_id}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to record vote: {e}")
            return False

    def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        """Get user preferences"""
        if not self.enabled:
            return None

        try:
            response = self.client.table("user_preferences").select("*").eq("user_id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Failed to get user preferences: {e}")
            return None

    def save_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Save/update user preferences"""
        if not self.enabled:
            return False

        try:
            # Try to update first
            response = self.client.table("user_preferences").update(preferences).eq("user_id", user_id).execute()

            # If nothing was updated, insert
            if not response.data:
                preferences["user_id"] = user_id
                self.client.table("user_preferences").insert(preferences).execute()

            print(f"[SUPABASE] Saved preferences for {user_id}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save preferences: {e}")
            return False

    def log_reading_history(self, story_id: int, user_id: Optional[str] = None,
                           time_spent_seconds: int = 0, expanded: bool = False) -> bool:
        """Log story reading"""
        if not self.enabled:
            return False

        try:
            self.client.table("reading_history").insert({
                "story_id": story_id,
                "user_id": user_id,
                "time_spent_seconds": time_spent_seconds,
                "expanded": expanded
            }).execute()

            return True
        except Exception as e:
            print(f"[ERROR] Failed to log reading: {e}")
            return False

    def get_latest_edition(self) -> Optional[Dict]:
        """Get the most recent edition"""
        if not self.enabled:
            return None

        try:
            response = self.client.table("editions").select("*").order("date", desc=True).limit(1).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Failed to get latest edition: {e}")
            return None

    def get_edition_stories(self, edition_id: int) -> List[Dict]:
        """Get all stories for an edition"""
        if not self.enabled:
            return []

        try:
            response = self.client.table("stories").select("*").eq("edition_id", edition_id).order("position", asc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Failed to get edition stories: {e}")
            return []

# Singleton instance
_client_instance = None

def get_supabase_client() -> SupabaseClient:
    """Get or create the Supabase client"""
    global _client_instance
    if _client_instance is None:
        _client_instance = SupabaseClient()
    return _client_instance
