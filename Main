import subprocess
import time

# 1. Initialize DB schema first
subprocess.run(["python3", "database.py"])

# 2. Launch all 3 daemons as sub-processes
watcher = subprocess.Popen(["python3", "watcher.py"])
miner = subprocess.Popen(["python3", "miner.py"])
cleaner = subprocess.Popen(["python3", "cleaner.py"])

print("All 3 Monkey Court agents successfully started online!")

# 3. Main process watchdog
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    watcher.terminate()
    miner.terminate()
    cleaner.terminate()
