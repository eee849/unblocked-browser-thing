import os
import subprocess
import sys
import threading
import time
from flask import Flask, Response

# Define required system packages
REQUIRED_PACKAGES = ["firefox", "xvfb", "x11vnc", "novnc", "wget", "unzip",
                     "xubuntu-desktop", "pulseaudio", "pavucontrol", "ffmpeg",
                     "sox", "python3-flask"]

PYTHON_PACKAGES = ["selenium", "pyvirtualdisplay"]

# Create Flask app for HTTP audio streaming
app = Flask(__name__)

# Function to ensure the custom-built D-Bus is used
def setup_dbus():
    print("🔄 Setting up custom D-Bus session...")

    # Set custom D-Bus paths (modify these if needed)
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/var/run/dbus/system_bus_socket"

    # Start a D-Bus session if not already running
    if not os.path.exists("/var/run/dbus/system_bus_socket"):
        subprocess.run(["mkdir", "-p", "/var/run/dbus"])
        subprocess.run(["dbus-daemon", "--config-file=/etc/dbus-1/system.conf", "--fork"])

    # Export D-Bus environment variables
    dbus_env = subprocess.run(["dbus-launch"], capture_output=True, text=True).stdout
    for line in dbus_env.splitlines():
        if line.startswith("DBUS_SESSION_BUS_ADDRESS") or line.startswith("DBUS_SESSION_BUS_PID"):
            key, value = line.split("=", 1)
            os.environ[key] = value.strip()

# Function to install system packages
def install_system_packages():
    print("🔍 Checking system dependencies...")
    subprocess.run(["sudo", "apt", "update"], check=True)
    
    for package in REQUIRED_PACKAGES:
        if subprocess.run(["which", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
            print(f"📦 Installing {package}...")
            subprocess.run(["sudo", "apt", "install", "-y", package], check=True)
        else:
            print(f"✅ {package} is already installed.")

# Function to install Python packages
def install_python_packages():
    print("🔍 Checking Python dependencies...")
    for package in PYTHON_PACKAGES:
        try:
            __import__(package)
            print(f"✅ {package} is already installed.")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

# Function to configure PulseAudio for HTTP audio streaming
def setup_audio():
    print("🔊 Setting up PulseAudio virtual audio device...")

    subprocess.run(["pulseaudio", "--start"], check=True)
    subprocess.run(["pactl", "load-module", "module-null-sink", "sink_name=VirtualSpeaker"], check=True)
    subprocess.run(["pactl", "set-default-sink", "VirtualSpeaker"], check=True)

# Function to start FFmpeg and stream audio over HTTP
def generate_audio():
    print("🎵 Starting FFmpeg audio capture...")

    ffmpeg_command = [
        "ffmpeg", "-f", "pulse", "-i", "VirtualSpeaker.monitor",
        "-acodec", "mp3", "-b:a", "128k", "-f", "mp3", "-"
    ]

    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Stream the output dynamically
    def stream():
        while True:
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            yield chunk

    return Response(stream(), mimetype="audio/mpeg")

# Default Home Page to Prevent 404 Errors
@app.route('/')
def home():
    return '''
    <h1>🎵 Audio Streaming Server</h1>
    <p>Click here to listen: <a href="/audio">Listen to Stream</a></p>
    '''

# Flask route to serve the audio stream
@app.route('/audio')
def audio_stream():
    return generate_audio()

# Function to start Flask HTTP server for audio streaming
def start_http_server():
    print("🌍 Starting Flask HTTP server for audio streaming...")
    app.run(host="0.0.0.0", port=8000, threaded=True)

# Function to start the VNC server with Xubuntu Desktop
def start_vnc():
    print("🖥️  Starting Xvfb virtual display on :99...")
    subprocess.Popen(["sudo", "Xvfb", ":99", "-screen", "0", "1920x1080x24", "-ac"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.environ["DISPLAY"] = ":99"
    time.sleep(2)  # Give Xvfb time to start

    print("🖥️  Starting Xubuntu Desktop (Xfce session)...")
    subprocess.Popen(["startxfce4"], env={"DISPLAY": ":99"}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)  # Give Xfce time to start

    print("🔄 Starting x11vnc server on port 5900...")
    subprocess.Popen(["x11vnc", "-display", ":99", "-nopw", "-forever", "-rfbport", "5900"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    print("🌐 Starting noVNC server on http://localhost:6080 ...")
    subprocess.Popen(["/usr/share/novnc/utils/launch.sh", "--vnc", "localhost:5900"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

# Main function to install dependencies and start services
def main():
    install_system_packages()
    install_python_packages()
    setup_dbus()  # Ensure custom-built D-Bus is used
    setup_audio()  # Enable HTTP audio streaming
    start_vnc()

    # Run Flask server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.start()

    print("🚀 Starting Firefox automation script...")
    subprocess.run(["python3", "themain.py"])

if __name__ == "__main__":
    main()
