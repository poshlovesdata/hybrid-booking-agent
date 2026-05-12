import sqlite3
import chromadb
import os
import shutil

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Define our mock workspaces
WORKSPACES = [
    {
        "id": "space_1",
        "name": "The Quiet Hub Ikeja",
        "location": "Ikeja",
        "base_capacity": 4,
        "price_per_hour": 5000,
        "vibe_description": "Extremely quiet environment perfect for deep work. Features reliable 24/7 backup power and an in-house barista serving excellent premium coffee. No loud talking allowed."
    },
    {
        "id": "space_2",
        "name": "Creative Collab Yaba",
        "location": "Yaba",
        "base_capacity": 10,
        "price_per_hour": 8000,
        "vibe_description": "Vibrant and energetic startup vibe. Comes with massive whiteboards, blazing fast fiber internet, and bean bag chairs. Great for brainstorming and team offsites."
    },
    {
        "id": "space_3",
        "name": "Executive Suites VI",
        "location": "Victoria Island",
        "base_capacity": 8,
        "price_per_hour": 15000,
        "vibe_description": "Premium, professional boardroom setup. Features high-end ergonomic chairs, a smart TV for presentations, and a beautiful ocean view. Very formal and corporate."
    },
    {
        "id": "space_4",
        "name": "Lekki Creator Studio",
        "location": "Lekki",
        "base_capacity": 2,
        "price_per_hour": 7000,
        "vibe_description": "Soundproofed room with aesthetic RGB lighting and natural light. Designed specifically for podcasting, video editing, and content creation. Very cozy."
    },
    {
        "id": "space_5",
        "name": "Ikeja Power Lounge",
        "location": "Ikeja",
        "base_capacity": 6,
        "price_per_hour": 6000,
        "vibe_description": "Open-plan desk space with guaranteed uninterrupted power supply (UPS + Gen). Good for networking and casual remote work. Has a self-service tea and coffee station."
    }
]

def seed_sqlite():
    """Populates the SQLite database with workspaces and mock bookings."""
    print("Seeding SQLite Database...")
    db_path = "data/inventory.db"
    
    # Remove existing DB to ensure a fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workspaces (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            base_capacity INTEGER NOT NULL,
            price_per_hour REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
        )
    ''')
    
    # Insert Workspaces
    for ws in WORKSPACES:
        cursor.execute(
            "INSERT INTO workspaces (id, name, location, base_capacity, price_per_hour) VALUES (?, ?, ?, ?, ?)",
            (ws["id"], ws["name"], ws["location"], ws["base_capacity"], ws["price_per_hour"])
        )
        
    # Insert Mock Bookings (To test the overlapping logic)
    # Let's assume the user will test for tomorrow (e.g., 2026-05-15)
    mock_bookings = [
        # space_1 is booked in the morning
        ("space_1", "2026-05-15", "10:00", "12:00"),
        # space_3 is booked all afternoon
        ("space_3", "2026-05-15", "13:00", "17:00"),
    ]
    
    for b in mock_bookings:
        cursor.execute(
            "INSERT INTO bookings (workspace_id, booking_date, start_time, end_time) VALUES (?, ?, ?, ?)", b
        )
        
    conn.commit()
    conn.close()
    print("SQLite Database seeded successfully!")

def seed_chromadb():
    """Populates ChromaDB with vector embeddings of the workspace vibes."""
    print("Seeding ChromaDB Vector Store...")
    chroma_path = "data/chroma_data"
    
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)
        
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.create_collection(name="workspace_vibes")
    
    ids = []
    documents = []
    metadatas = []
    
    for ws in WORKSPACES:
        ids.append(ws["id"])
        documents.append(ws["vibe_description"])
        # Adding location to metadata so we can pre-filter before semantic search
        metadatas.append({"location": ws["location"]})
        
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("ChromaDB Vector Store seeded successfully!")

if __name__ == "__main__":
    print("Starting Data Initialization...")
    seed_sqlite()
    seed_chromadb()
    print("\nAll data seeded! You are ready to run the FastAPI server.")