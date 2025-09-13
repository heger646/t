import subprocess
import sys

# Launch both servers concurrently
http_proc = subprocess.Popen([sys.executable, "http_server.py"])
ftp_proc = subprocess.Popen([sys.executable, "ftp_server.py"])

print("Both servers started. Press Ctrl+C to stop.")

try:
    http_proc.wait()
    ftp_proc.wait()
except KeyboardInterrupt:
    print("Stopping servers...")
    http_proc.terminate()
    ftp_proc.terminate()
