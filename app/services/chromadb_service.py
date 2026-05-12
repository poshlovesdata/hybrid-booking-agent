import chromadb
from typing import List

chroma_client = chromadb.PersistentClient(path="./data/chroma_data")

# Get or create the collection that holds our workspace descriptions
collection = chroma_client.get_or_create_collection(name="workspace_vibes")

def search_semantic_vibe(vibe_keywords: List[str], location: str, n_results: int = 3) -> List[str]:
    """
    Takes the user's vibe keywords, converts them to a single query string,
    and searches ChromaDB for the closest matching workspaces in the target location.
    Returns a list of workspace IDs.
    """
    # If the LLM couldn't find any vibe keywords, return a wildcard search or empty list
    if not vibe_keywords:
        query_text = "workspace office desk environment"
    else:
        query_text = f"Looking for a space with: {', '.join(vibe_keywords)}"
    
    # Execute the semantic search against ChromaDB
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"location": location} if location else None 
    )
    
    if results['ids'] and len(results['ids'][0]) > 0:
        return results['ids'][0]
    
    return []