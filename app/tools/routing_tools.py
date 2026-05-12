from typing import List, Dict
from app.services.sqlite_service import check_live_availabilty
from app.services.chromadb_service import search_semantic_vibe

def tool_find_vibes(vibe_keywords: List[str], location: str) -> List[str]:
    """
    AI Tool: The AI should call this FIRST to get a list of workspace IDs 
    that match the user's semantic needs (e.g., "quiet", "good coffee").
    """
    return search_semantic_vibe(vibe_keywords, location)
    
def tool_check_availability(workspace_ids: List[str], date: str, start_time: str, duration: int, capacity: int) -> List[Dict]:
    """
    AI Tool: The AI should call this SECOND. 
    It passes the IDs from the first tool here to verify they aren't double-booked.
    """
    
    return check_live_availabilty( item_ids=workspace_ids, 
        requested_date=date, 
        start_time=start_time, 
        duration_hours=duration, 
        capacity_needed=capacity)