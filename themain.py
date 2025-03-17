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
firefox_options.add_argument("-private")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
firefox_options.set_preference("general.useragent.override", user_agent)
firefox_options.set_preference("dom.webdriver.enabled", False)
firefox_options.set_preference("useAutomationExtension", False)
firefox_options.set_preference("webgl.disabled", False)
firefox_options.set_preference("gfx.font_rendering.directwrite.enabled", True)

 #ensure that there are no webdriver lock problems from past experience
  # Ensure it starts maximized
# Remove headless mode (important for GUI!)
# firefox_options.add_argument("--headless")  # COMMENT THIS LINE!

# Setup Firefox WebDriver
service = Service("/usr/bin/geckodriver")  # Make sure geckodriver is installed
driver = webdriver.Firefox(service=service, options=firefox_options)

# Open a website
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
