import os
import subprocess
import time
import threading
from flask import Flask, Response
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

app = Flask(__name__)

# ✅ Set the correct home directory for Codespaces
CODESPACES_HOME = "/workspaces/unblocked-browser-thing"

# Function to initialize and install Alpine Linux with a desktop environment
def install_alpine_linux():
    print("🐧 Setting up Alpine Linux in a Docker container...")
    
    # Check if the Alpine container already exists
    container_check = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
    if "alpine-desktop" in container_check.stdout:
        print("✅ Alpine Linux container already exists. Starting...")
        subprocess.run(["docker", "start", "alpine-desktop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("🚀 Creating and initializing Alpine Linux container...")
        subprocess.run(["docker", "run", "-dit", "--name", "alpine-desktop", "--privileged", "-p", "6080:6080", "-p", "5900:5900", "alpine"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Install required Alpine packages
        subprocess.run(["docker", "exec", "alpine-desktop", "apk", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["docker", "exec", "alpine-desktop", "apk", "add", "xfce4", "xfce4-terminal", "xfce4-panel", "xfce4-session", "xfce4-settings", "dbus", "x11vnc", "tigervnc", "novnc", "firefox-esr", "geckodriver", "supervisor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Configure VNC
        subprocess.run(["docker", "exec", "alpine-desktop", "sh", "-c", "mkdir -p ~/.vnc && echo 'xfce4-session &' > ~/.vnc/xstartup && chmod +x ~/.vnc/xstartup"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ Alpine Linux desktop environment is set up!")

# Function to start Alpine desktop environment with VNC & NoVNC
def start_alpine_desktop():
    print("🖥️  Starting Alpine Linux XFCE desktop in Docker with VNC & NoVNC...")
    
    # Start the X server and desktop session
    subprocess.run(["docker", "exec", "-d", "alpine-desktop", "sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 &"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "exec", "-d", "alpine-desktop", "sh", "-c", "export DISPLAY=:99 && startxfce4 &"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Start the VNC server inside the Alpine container
    subprocess.run(["docker", "exec", "-d", "alpine-desktop", "sh", "-c", "x11vnc -forever -display :99 -rfbport 5900 &"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Start NoVNC to allow remote access via the browser
    subprocess.run(["docker", "exec", "-d", "alpine-desktop", "sh", "-c", "novnc --listen 6080 --vnc localhost:5900 &"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Verify if the services are running
    subprocess.run(["docker", "exec", "alpine-desktop", "sh", "-c", "ps aux | grep -E 'x11vnc|novnc|startxfce4'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to start Flask HTTP server for audio streaming
def start_http_server():
    print("🌍 Starting Flask HTTP server for audio streaming...")
    app.run(host="0.0.0.0", port=8000, threaded=True)

# Function to start Selenium WebDriver in Alpine Linux (GUI mode, no headless)
def start_selenium():
    print("🚀 Starting Selenium WebDriver with Firefox inside Alpine Docker (GUI mode)...")
    
    # Set display for GUI mode
    os.environ["DISPLAY"] = ":99"
    
    firefox_options = Options()
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    firefox_options.add_argument("--start-maximized")
    firefox_options.add_argument("-private")
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    firefox_options.set_preference("general.useragent.override", user_agent)
    firefox_options.set_preference("dom.webdriver.enabled", False)
    firefox_options.set_preference("useAutomationExtension", False)
    firefox_options.set_preference("webgl.disabled", False)
    firefox_options.set_preference("gfx.font_rendering.directwrite.enabled", True)

    # Set the correct paths for Geckodriver inside Alpine
    service = Service("/usr/bin/geckodriver")
    
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get("https://www.google.com")
    print("✅ Google loaded successfully.")
    
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import random
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("https://youtube.com")
    time.sleep(random.uniform(1, 3))  # Random delay to simulate typing
    search_box.send_keys(Keys.ENTER)
    
    # Keep the browser open for debugging
    input("Press Enter to quit...")
    
    # Close browser
    driver.quit()

# Main function
def main():
    install_alpine_linux()
    start_alpine_desktop()
    
    # Run Flask server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.start()

    start_selenium()

if __name__ == "__main__":
    main()