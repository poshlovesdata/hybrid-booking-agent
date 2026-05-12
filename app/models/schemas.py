from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


    

class InventoryItem(BaseModel):
    """Represents a single bookable item (e.g., workspace, equipment)"""
    id: str
    name: str
    location: str
    base_capacity: int
    price_per_hour: float
    
class SearchIntent(BaseModel):
    """The structured constraints extracted from the user's natural language prompt"""
    location: Optional[str] = Field(description="The desired city or neighborhood")
    req_capacity: Optional[int] = Field(default=1, description="Number of people needing the space")
    date: Optional[str] = Field(default=None, description="Requested date in YYYY-MM-DD format")
    start_time: Optional[str] = Field(default=None, description="Requested start time in HH:MM format")
    end_time: Optional[str] = Field(default=None, description="Requested end time in HH:MM format")
    duration_hours: Optional[int] = Field(default=1, description="How many hours they need the space")
    vibe: List[str] = Field(default_factory=list, description="A list of keywords for the vibe/semantic search (e.g. 'quiet', 'coffee')")
    
class WorkspaceRecommendation(BaseModel):
    """A single verified recommendation"""
    workspace_id: str
    name: str
    price_per_hour: float | None = Field(default=None, description="The base hourly rate of the workspace.")
    total_price: float | None = Field(description="The exact total_price returned by the check_live_availability tool. DO NOT calculate this yourself.")
    vibe_match_reason: str = Field(description="Detailed explanation of why this space matches the user's vibe keywords")
    availability_status: bool | None

class FinalResponse(BaseModel):
    """The strict JSON output the AI must return to the frontend"""
    agent_messge: str = Field(description="A brief conversational reply summarizing the findings or explaining compromises")
    recommendations: List[WorkspaceRecommendation] = Field(default_factory=list, description="List of available spaces. Must be empty if none are available.")
        
        
    
