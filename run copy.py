import os
import subprocess
import time

def start_vnc():
    print("🖥️  Starting Xvfb virtual display on :99...")
    subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1920x1080x24", "-ac"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.environ["DISPLAY"] = ":99"
    time.sleep(2)  # Give Xvfb time to start

    print("🔄 Starting x11vnc server on port 5900...")
    subprocess.Popen(["x11vnc", "-display", ":99", "-nopw", "-forever", "-rfbport", "5900"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    print("🌐 Starting NoVNC on http://localhost:6080 ...")
    subprocess.Popen(["/usr/share/noVNC/utils/websockify/run", "6080", "localhost:5900"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

def start_firefox():
    print("🔥 Launching Firefox inside Xvfb session...")
    subprocess.Popen(["firefox"], env={"DISPLAY": ":99"}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

if __name__ == "__main__":
    start_vnc()
    start_firefox()
    print("✅ Everything is running! Open NoVNC at: http://localhost:6080")
    input("Press Enter to exit...")  # Keeps script running
