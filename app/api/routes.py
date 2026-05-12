from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from loguru import logger
from pydantic_ai.messages import ModelMessage

from app.models.schemas import FinalResponse
from app.services.agent import process_user_query

# Initialize the router
router = APIRouter()
session_memory: dict[str, list[ModelMessage]] = {}


class ChatRequest(BaseModel):
    """The incoming JSON payload from the frontend"""
    session_id: str = Field(default="default_user", description="Unique ID for the user session to track memory")
    user_prompt: str

@router.post("/search", response_model=FinalResponse)
async def search_workspaces(request: ChatRequest):
    """
    Receives a natural language query, passes it to the AI Routing Engine,
    and returns a structured list of available workspaces.
    """
    try:
        
        # Fetch existing memory for this user (or an empty list if new)
        history = session_memory.get(request.session_id, [])
        
        from app.services.agent import agent
        result = await agent.run(request.user_prompt, message_history=history)
        
        full_history = result.all_messages()
        session_memory[request.session_id] = full_history[-10:]
        
        return result.output
    
        # # Await the async execution of the PydanticAI agent
        # result = await process_user_query(request.user_prompt)
        # return result
        
    except Exception as e:
        logger.error(f"Error processing user query: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="The AI routing engine encountered an error while processing your request."
        )