import os
import subprocess
import time
import threading
from flask import Flask, Response

app = Flask(__name__)

# ✅ Set the correct home directory for Codespaces
CODESPACES_HOME = "/workspaces/unblocked-browser-thing"

# Function to start virtual display
def start_xvfb():
    print("🖥️  Starting Xvfb virtual display on :99...")
    subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1920x1080x24", "-ac"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.environ["DISPLAY"] = ":99"
    time.sleep(2)

# Function to start Xubuntu Desktop (ignoring D-Bus in Codespaces)
def start_xubuntu():
    print("🖥️  Starting Xubuntu Desktop (Xfce session)...")

    os.environ["HOME"] = "/workspaces/unblocked-browser-thing"
    os.environ["XDG_RUNTIME_DIR"] = f"{os.environ['HOME']}/.xdg-runtime"
    os.makedirs(os.environ["XDG_RUNTIME_DIR"], exist_ok=True)

    # ❌ Prevent startxfce4 from launching dbus
    xfce_process = subprocess.Popen(
        ["startxfce4", "--disable-server", "--sm-client-disable"],
        env={"DISPLAY": ":99", "HOME": os.environ["HOME"], "XDG_RUNTIME_DIR": os.environ["XDG_RUNTIME_DIR"], "DBUS_SESSION_BUS_ADDRESS": "none"},
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(5)

    if xfce_process.poll() is not None:
        output, error = xfce_process.communicate()
        print(f"❌ Xubuntu Error: {error.decode()}")
        exit(1)

# Function to start VNC server
def start_vnc():
    print("🔄 Starting x11vnc server on port 5900...")
    subprocess.Popen(["x11vnc", "-display", ":99", "-nopw", "-forever", "-ncache", "10", "-rfbport", "5900"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    print("🌐 Starting noVNC server on http://localhost:6080 ...")
    subprocess.Popen(["/usr/share/novnc/utils/launch.sh", "--vnc", "localhost:5900"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

# Function to start Flask HTTP server for audio streaming
def start_http_server():
    print("🌍 Starting Flask HTTP server for audio streaming...")
    app.run(host="0.0.0.0", port=8000, threaded=True)

# Main function
def main():
    start_xvfb()
    start_xubuntu()
    start_vnc()

    # Run Flask server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.start()

    print("🚀 Starting Firefox automation script...")
    subprocess.run(["python3", "themain.py"])

if __name__ == "__main__":
    main()
