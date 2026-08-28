import sqlite3
import time

def process_next_task():
    conn = sqlite3.connect("monkey_court.db", timeout=10)
    cursor = conn.cursor()
    
    # Atomic selection to claim a pending task safely
    cursor.execute("""
        SELECT id, payload FROM task_queue 
        WHERE status = 'PENDING' 
        ORDER BY id ASC LIMIT 1
    """)
    row = cursor.fetchone()
    
    if row:
        task_id, payload = row
        cursor.execute("UPDATE task_queue SET status = 'MINING' WHERE id = ?", (task_id,))
        conn.commit()
        
        # Execute work
        time.sleep(2) 
        
        cursor.execute("UPDATE task_queue SET status = 'COMPLETED' WHERE id = ?", (task_id,))
        conn.commit()
    
    conn.close()

if __name__ == "__main__":
    while True:
        process_next_task()
        time.sleep(5)
