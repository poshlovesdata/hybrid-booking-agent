from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title="AI Routing Engine",
    description="Multi-agent search and booking API combining Semantic Search with deterministic SQL validation.",
)

# Enable CORS for the local UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api", tags=["AI Routing"])

@app.get("/", tags=["Health"])
async def health_check():
    """
    A simple health check endpoint to verify the server is running.
    """
    return {"status": "online", "message": "Hybrid Routing Engine is active."}