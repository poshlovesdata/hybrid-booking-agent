from pydantic_ai import Agent
from app.models.schemas import FinalResponse, SearchIntent, InventoryItem
from app.tools.routing_tools import tool_find_vibes, tool_check_availability

SYSTEM_PROMPT = """
You an AI Routing Engine.
Your job is to parse a user's request for a workspace and return the best available option.

Workflow:
1. Extract the constraints (Location, Capacity, Time, and Vibe).
2. Use the 'tool_find_vibes' tool to get a list of semantically relevant workspace IDs.
3. CRITICAL: You must pass those IDs into the 'tool_check_availability' tool to ensure they are free.
4. Never recommend a space without checking availability.
5. If the first choices are booked, explain that in your message and offer the next best available option.

Return your final answer matching the expected schema.
"""


agent = Agent(model='openai:gpt-4o', output_type=FinalResponse, system_prompt=SYSTEM_PROMPT, tools=[tool_find_vibes, tool_check_availability])


async def process_user_query(user_prompt: str) -> FinalResponse:
    """
    This is the main entry point for FastAPI backend
    """
    result = await agent.run(user_prompt)
    
    # contains the validated FinalResponse Pydantic object
    return result.output