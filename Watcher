import sqlite3
import time

def add_task(task_type, payload):
    conn = sqlite3.connect("monkey_court.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO task_queue (task_type, payload) VALUES (?, ?)",
        (task_type, payload)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        # Example polling loop: queues a task every 30 seconds
        add_task("FETCH_DATA", "sample_payload_data")
        time.sleep(30)
