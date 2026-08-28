import os
import subprocess
import time

# --- 1. START HTTP SERVER FIRST FOR RENDER HEALTH CHECK ---
try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading

    class HealthHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Monkey Court Online")

        def log_message(self, format, *args):
            return  # Suppress HTTP access logs

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"Health check server listening on 0.0.0.0:{port}")
except Exception as e:
    print(f"Server warning: {e}")

# --- 2. INITIALIZE DATABASE ---
subprocess.run(["python", "database.py"])

# --- 3. LAUNCH THREE MONKEY AGENTS ---
watcher = subprocess.Popen(["python", "watcher.py"])
miner = subprocess.Popen(["python", "miner.py"])
cleaner = subprocess.Popen(["python", "cleaner.py"])

print("All 3 Monkey Court agents successfully started online!")

# --- 4. KEEP ALIVE ---
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    watcher.terminate()
    miner.terminate()
    cleaner.terminate()
