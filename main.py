import os
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# 1. Bind an HTTP server so Render's Free Web Service scanner succeeds
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Three Monkey System is Active!")

def run_dummy_server():
    # Read assigned PORT environment variable, default to 10000
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Start HTTP server on host 0.0.0.0 in a daemon thread
threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. Initialize DB schema
subprocess.run(["python", "database.py"])

# 3. Launch sub-processes
watcher = subprocess.Popen(["python", "watcher.py"])
miner = subprocess.Popen(["python", "miner.py"])
cleaner = subprocess.Popen(["python", "cleaner.py"])

print("All 3 Monkey Court agents successfully started online!")

# 4. Keep main process alive
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    watcher.terminate()
    miner.terminate()
    cleaner.terminate()
