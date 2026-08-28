import os
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# 1. Ultra-light HTTP server returning minimal output to satisfy cron-job.org
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"OK")  # 2 bytes output (prevents 'output too large' errors)

    def log_message(self, format, *args):
        return  # Silence HTTP server logs to keep terminal logs clean

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. Initialize DB schema
subprocess.run(["python", "database.py"])

# 3. Launch sub-processes
watcher = subprocess.Popen(["python", "watcher.py"])
miner = subprocess.Popen(["python", "miner.py"])
cleaner = subprocess.Popen(["python", "cleaner.py"])

print("All 3 Monkey Court agents successfully started online!")

# 4. Main loop watchdog
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    watcher.terminate()
    miner.terminate()
    cleaner.terminate()
