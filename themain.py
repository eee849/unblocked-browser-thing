import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set display for GUI mode
subprocess.run("export DISPLAY=:99", shell=True)
os.environ["DISPLAY"] = ":99"

# Configure Firefox options
firefox_options = Options()
firefox_options.add_argument("--width=1920")
firefox_options.add_argument("--height=1080")
firefox_options.add_argument("--start-maximized")
firefox_options.add_argument("-private") #ensure that there are no webdriver lock problems from past experience
  # Ensure it starts maximized
# Remove headless mode (important for GUI!)
# firefox_options.add_argument("--headless")  # COMMENT THIS LINE!

# Setup Firefox WebDriver
service = Service("/usr/bin/geckodriver")  # Make sure geckodriver is installed
driver = webdriver.Firefox(service=service, options=firefox_options)

# Open a website
driver.get("https://www.google.com")
print("✅ Google loaded successfully.")

# Keep the browser open for debugging
input("Press Enter to quit...")

# Close browser
driver.quit()
