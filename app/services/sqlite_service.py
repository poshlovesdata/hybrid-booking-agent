import sqlite3
from typing import List, Dict
from loguru import logger


DB_FILE = 'data/inventory.db'

def get_db_connection():
    """Establish and return a connection to the local SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    logger.info(f"Succesfully connected to {DB_FILE}")
    return conn
    

def setup_database():
    """Create the necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
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
            booking_date TEXT NOT NULL, -- Format: YYYY-MM-DD
            start_time TEXT NOT NULL,   -- Format: HH:MM
            end_time TEXT NOT NULL,     -- Format: HH:MM
            FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_bookings_date_workspace 
        ON bookings(booking_date, workspace_id)
    ''')

    conn.commit()
    conn.close()

def check_live_availabilty(item_ids: List[str], start_time: str, duration_hours: int, requested_date: str, capacity_needed: int) -> List[Dict]:
    """
    Takes a list of semantically matched IDs and checks the live database 
    to filter out any that are already booked for the requested time.
    """
    if not item_ids:
        logger.info("No matching workspace ids for availability check; returning empty list")
        return []

    conn = get_db_connection()
    cursor = conn.cursor()
    
    start_hour, start_minute = map(int, start_time.split(':'))
    end_time_str = f"{start_hour + duration_hours:02d}:{start_minute:02d}"
    
    placeholders = ','.join(['?'] * len(item_ids))
    
    query = f"""
    SELECT 
        w.id as workspace_id,
        w.name,
        w.price_per_hour,
        (w.price_per_hour * ?) as total_price
    FROM workspaces w
    WHERE w.id IN ({placeholders}) 
    AND w.base_capacity >= ?
    AND w.id NOT IN (
        SELECT workspace_id
        FROM bookings
        WHERE booking_date = ?
        AND (
                (start_time <= ? AND end_time > ?) OR  -- New booking starts during an existing one
                (start_time < ? AND end_time >= ?) OR  -- New booking ends during an existing one
                (start_time >= ? AND end_time <= ?)    -- New booking is completely inside an existing one
            )
    )
    """
    
    params = (
        duration_hours,
        *item_ids,
        capacity_needed,
        requested_date,
        start_time, start_time,
        end_time_str, end_time_str,
        start_time, end_time_str
    )
    
    
    cursor.execute(query, params)
    
    available_spaces = [ dict(row) for row in cursor.fetchall()]
    
    conn.close()

    if not available_spaces:
        logger.info(
            f"No available workspaces for date={requested_date} time={start_time} "
            f"duration={duration_hours}h capacity={capacity_needed}"
        )
    
    return available_spaces

def get_basic_workspace_details(item_ids: List[str]) -> List[Dict]:
    """
    Retrieves basic workspace info (name) without checking time availability.
    Used for 'Discovery Mode' when the user hasn't provided dates yet.
    """
    if not item_ids:
        return []
        
    conn = get_db_connection()
    cursor = conn.cursor()
    placeholders = ','.join(['?'] * len(item_ids))
    
    query = f"SELECT id as workspace_id, name, price_per_hour FROM workspaces WHERE id IN ({placeholders})"
    cursor.execute(query, tuple(item_ids))
    details = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return details