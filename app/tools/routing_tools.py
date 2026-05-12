import asyncio
from typing import List, Dict
from app.services.sqlite_service import check_live_availabilty
from app.services.sqlite_service import get_basic_workspace_details
from app.services.chromadb_service import search_semantic_vibe

async def tool_find_vibes(vibe_keywords: List[str], location: str) -> List[str]:
    """
    AI Tool: The AI should call this FIRST to get a list of workspace IDs 
    that match the user's semantic needs (e.g., "quiet", "good coffee").
    """
    return await asyncio.to_thread(search_semantic_vibe, vibe_keywords, location)

async def tool_get_workspace_details(workspace_ids: List[str]) -> List[Dict]:
    """
    AI Tool: Use this if the user HAS NOT provided a date/time. 
    It gets the names of the workspaces so you can show them to the user.
    """
    return await asyncio.to_thread(get_basic_workspace_details, workspace_ids)
    
async def tool_check_availability(workspace_ids: List[str], date: str, start_time: str, duration: int, capacity: int) -> List[Dict]:
    """
    AI Tool: The AI should call this SECOND. 
    It passes the IDs from the first tool here to verify they aren't double-booked.
    """
    
    return await asyncio.to_thread(
        check_live_availabilty,
        workspace_ids, start_time, duration, date, capacity
    )