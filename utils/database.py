import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "aquasentinel.db"
)


def get_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # User management
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # Monitoring locations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            district TEXT NOT NULL,
            location_name TEXT NOT NULL
        )
    """)

    # Water quality measurements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            sample_date TEXT NOT NULL,
            ph REAL,
            turbidity REAL,
            tds REAL,
            dissolved_oxygen REAL,
            bod REAL,
            water_source TEXT,
            FOREIGN KEY(location_id) REFERENCES locations(id)
        )
    """)

    # Image analysis history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT,
            detection_result TEXT,
            confidence REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            description TEXT,
            severity TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create a default administrator account if one does not exist.
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, ("admin", "admin123", "admin"))

    connection.commit()
    connection.close()

    print("AquaSentinel AI database initialized successfully!")


if __name__ == "__main__":
    initialize_database()