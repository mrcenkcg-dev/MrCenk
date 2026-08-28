import sqlite3
import time

def cleanup():
    conn = sqlite3.connect("monkey_court.db", timeout=10)
    cursor = conn.cursor()
    # Purge completed tasks older than 1 hour to keep storage tiny
    cursor.execute("""
        DELETE FROM task_queue 
        WHERE status = 'COMPLETED' 
        AND updated_at < datetime('now', '-1 hour')
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        cleanup()
        time.sleep(3600)  # Runs every hour
