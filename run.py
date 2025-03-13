import os
import subprocess
import time

# Configuration
VNC_PASSWORD = "mypassword"  # Change this to your desired VNC password
DISPLAY_NUM = ":1"
VNC_PORT = "5901"
WEBSOCKIFY_PORT = "6080"

def kill_existing_processes():
    """ Kill existing Xvfb, x11vnc, and websockify processes to prevent conflicts """
    subprocess.run("pkill Xvfb || true", shell=True)
    subprocess.run("pkill x11vnc || true", shell=True)
    subprocess.run("pkill websockify || true", shell=True)

def start_xvfb():
    """ Start Xvfb virtual display """
    print("🖥️ Starting Xvfb...")
    subprocess.Popen(f"Xvfb {DISPLAY_NUM} -screen 0 1920x1080x24 &", shell=True)
    os.environ["DISPLAY"] = DISPLAY_NUM
    time.sleep(2)  # Give Xvfb time to start

def start_x11vnc():
    """ Start x11vnc server """
    print("🔄 Starting x11vnc...")
    cmd = f"x11vnc -create -forever -display {DISPLAY_NUM} -passwd {VNC_PASSWORD} -rfbport {VNC_PORT} -noxdamage -repeat &"
    subprocess.Popen(cmd, shell=True)
    time.sleep(2)  # Give x11vnc time to start

def start_websockify():
    """ Start websockify for noVNC """
    print("🌐 Starting websockify (noVNC)...")
    subprocess.Popen(f"websockify --web /usr/share/novnc {WEBSOCKIFY_PORT} localhost:{VNC_PORT} &", shell=True)
    time.sleep(2)  # Give websockify time to start

def print_connection_info():
    """ Print instructions for connecting to the VNC session """
    print("\n✅ VNC & Web Interface Started!")
    print(f"🔹 **VNC Connection:** `your-github-codespace-url:{VNC_PORT}`")
    print(f"🌍 **noVNC (Browser Access):** `http://your-github-codespace-url:{WEBSOCKIFY_PORT}/vnc.html`")
    print("🔑 **VNC Password:**", VNC_PASSWORD)

if __name__ == "__main__":
    kill_existing_processes()
    start_xvfb()
    start_x11vnc()
    start_websockify()
    print_connection_info()

    print("\n🚀 Your remote desktop environment is now running!")
    print("🔴 Press **CTRL+C** to stop the VNC session.")
    
    # Keep script running to prevent processes from stopping
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Stopping VNC session...")
        kill_existing_processes()
