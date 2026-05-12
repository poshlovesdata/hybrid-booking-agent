import asyncio
from typing import List, Dict
from loguru import logger
from app.services.sqlite_service import check_live_availabilty
from app.services.sqlite_service import get_basic_workspace_details
from app.services.chromadb_service import search_semantic_vibe

async def tool_find_vibes(vibe_keywords: List[str], location: str) -> List[str]:
    """
    AI Tool: The AI should call this FIRST to get a list of workspace IDs 
    that match the user's semantic needs (e.g., "quiet", "good coffee").
    """
    logger.info(f"Tool called: tool_find_vibes | Keywords: {vibe_keywords} | Location: {location}")
    return await asyncio.to_thread(search_semantic_vibe, vibe_keywords, location)

async def tool_get_workspace_details(workspace_ids: List[str]) -> List[Dict]:
    """
    AI Tool: Use this if the user HAS NOT provided a date/time. 
    It gets the names of the workspaces so you can show them to the user.
    """
    logger.info(f"Tool called: tool_get_workspace_details | Workspace IDs: {workspace_ids}")
    return await asyncio.to_thread(get_basic_workspace_details, workspace_ids)
    
async def tool_check_availability(workspace_ids: List[str], date: str, start_time: str, duration: int, capacity: int) -> List[Dict]:
    """
    AI Tool: The AI should call this SECOND. 
    It passes the IDs from the first tool here to verify they aren't double-booked.
    """
    logger.info(f"Tool called: tool_check_availability | Workspace IDs: {workspace_ids} | Date: {date} | Time: {start_time} | Duration: {duration}h | Capacity: {capacity}")
    return await asyncio.to_thread(
        check_live_availabilty,
        workspace_ids, start_time, duration, date, capacity
    )