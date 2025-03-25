import os
import subprocess
import sys
import time

# Define required system packages
REQUIRED_PACKAGES = ["firefox", "xvfb", "x11vnc", "novnc", "wget", "unzip"]
PYTHON_PACKAGES = ["selenium", "pyvirtualdisplay"]

# Function to install system packages
def install_system_packages():
    print("🔍 Checking system dependencies...")
    for package in REQUIRED_PACKAGES:
        if subprocess.run(["which", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
            print(f"📦 Installing {package}...")
            subprocess.run(["sudo", "apt", "update"], check=True)
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

# Function to install geckodriver
def install_geckodriver():
    print("🔍 Checking for geckodriver...")
    geckodriver_path = "/usr/bin/geckodriver"
    
    if not os.path.exists(geckodriver_path):
        print("📦 Installing geckodriver...")
        gecko_version = subprocess.run(
            ["wget", "-qO-", "https://api.github.com/repos/mozilla/geckodriver/releases/latest"],
            capture_output=True, text=True
        )
        try:
            version = gecko_version.stdout.split('"tag_name": "v')[1].split('"')[0]
        except IndexError:
            print("❌ Error fetching geckodriver version. Using latest stable.")
            version = "latest"

        geckodriver_url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-linux64.tar.gz"
        subprocess.run(["wget", geckodriver_url, "-O", "geckodriver.tar.gz"], check=True)
        subprocess.run(["tar", "-xvzf", "geckodriver.tar.gz"], check=True)
        subprocess.run(["sudo", "mv", "geckodriver", "/usr/bin/geckodriver"], check=True)
        subprocess.run(["chmod", "+x", "/usr/bin/geckodriver"], check=True)
        print(f"✅ Installed geckodriver {version}")
    else:
        print("✅ geckodriver is already installed.")

# Function to start the VNC server
# Function to start the VNC server
def start_vnc():
    print("🛑 Killing any existing Xvfb, x11vnc, and noVNC processes...")
    subprocess.run(["pkill", "-9", "Xvfb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-9", "x11vnc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-9", "websockify"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("🖥️  Starting Xvfb virtual display on :99...")
    subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1920x1080x24", "-ac"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.environ["DISPLAY"] = ":99"
    time.sleep(2)  # Give Xvfb time to start

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
    install_geckodriver()
    start_vnc()

    print("🚀 Starting Firefox automation script...")
    subprocess.run(["python3", "themain.py"])

if __name__ == "__main__":
    main()
