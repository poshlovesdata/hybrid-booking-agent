from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="AI Routing Engine",
    description="Multi-agent search and booking API combining Semantic Search with deterministic SQL validation.",
)

app.include_router(api_router, prefix="/api", tags=["AI Routing"])

@app.get("/", tags=["Health"])
async def health_check():
    """
    A simple health check endpoint to verify the server is running.
    """
    return {"status": "online", "message": "Hybrid Routing Engine is active."}