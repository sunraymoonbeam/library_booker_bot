import os
import random
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth
from datetime import datetime

# Module docstring
"""
This module provides utility functions for initializing a Selenium WebDriver
with specific configurations and stealth settings for web scraping.
"""

# User agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

def initialize_driver():
    """
    Initializes and returns a Chrome WebDriver with custom options and
    stealth settings to mimic a real user browser and avoid detection.
    
    Returns:
        WebDriver: An instance of Chrome WebDriver with specified options.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  # Start browser maximized
    options.add_argument(f"user-agent={random.choice(user_agents)}") # Randomly select a user agent from the list to mimic different browsers
    options.add_argument("--disable-dev-shm-usage") # Avoid crash issues in Docker containers
    options.add_argument("--no-sandbox")  # Bypass OS security model
    #options.add_argument("--headless") # Run Chrome in headless mode (without GUI)

    # Disable automation flags to avoid detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # # Set binary location if running in a non-standard environment
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "")
    # service = Service(os.environ.get("CHROMEDRIVER_PATH", ""))
    # driver = webdriver.Chrome(service=service, options=options)

    # driver_path = "path/to/driver" # Path to the Chrome WebDriver binary executable
    # service = Service(driver_path) 
    # driver = webdriver.Chrome(service=service, options=options)

    # Apply stealth settings to make automated browsing more human-like
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    
    return driver

def convert_str_datetime(time_str: str) -> datetime:
    """
    Converts a string representing time in 24-hour format into a datetime object for the current date.

    Parameters:
    - time_str (str): The time in 24-hour format as a string (e.g., "0800" for 8 AM).

    Returns:
    - datetime: A datetime object representing today's date at the specified hour and minute.

    Raises:
    - ValueError: If the input string is not in the correct format or represents an invalid time.
    """
    if len(time_str) != 4 or not time_str.isdigit():
        raise ValueError("Time must be a 4-digit string in 24-hour format (e.g., '0800').")

    hour = int(time_str[:2])
    minute = int(time_str[2:])

    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        raise ValueError("Hour must be between 00 and 23, and minute between 00 and 59.")

    return datetime(datetime.today().year, datetime.today().month, datetime.today().day, hour, minute)


def save_screenshot(driver: WebDriver, output_folder: str, username: str) -> None:
    """
    Saves a screenshot of the current browser window to a specified directory.

    The screenshot is saved within a directory named after the current date, and the
    filename includes the username and the current time to ensure uniqueness.

    Args:
        driver (WebDriver): The web driver instance used to take the screenshot.
        output_folder (str): The base directory where the screenshot will be saved.
        username (str): The username to include in the screenshot's filename.

    Returns:
        None
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H-%M')
    # Ensure the directory exists
    directory_path = os.path.join(output_folder, current_date)
    os.makedirs(directory_path, exist_ok=True)
    # Construct the full path for the screenshot
    filename = f"{username}-{current_time}-resource.png"
    full_screenshot_path = os.path.join(directory_path, filename)
    # Save the screenshot
    driver.save_screenshot(full_screenshot_path)


def save_metadata(output_folder: str, username: str, start_slot_time: datetime, end_slot_time: datetime, location: str, resource_category: str, resource_id: str) -> None:
    """
    Saves booking metadata to a CSV file in a more efficient and error-resistant manner.
     Args:
        username (str): Username of the user who made the booking.
        start_slot_time (datetime): The start time of the booking slot.
        end_slot_time (datetime): The end time of the booking slot.
        location (str): The location where the booking is made.
        resource_category (str): The category of the booked resource.
        resource_id (str): The ID of the booked resource.
        output_folder (str): The folder where the CSV file will be saved.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Define the CSV file path
    csv_file_path = os.path.join(output_folder, "booking_log.csv")
    
    # Determine if the file exists to decide on writing the header
    file_exists = os.path.isfile(csv_file_path)
    
    # Define the header and data
    header = ['username', 'booking_date', 'time_slot_start', 'time_slot_end', 'location', 'resource_category', 'resource_id']
    data = [username, datetime.now().strftime('%Y-%m-%d'), start_slot_time.strftime('%Y-%m-%d %H:%M'), end_slot_time.strftime('%Y-%m-%d %H:%M'), location, resource_category, resource_id]
    
    try:
        # Open the file in append mode if exists, else write mode
        with open(csv_file_path, 'a' if file_exists else 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header if the file did not exist
            if not file_exists:
                writer.writerow(header)
            writer.writerow(data)
    except Exception as e:
        # Log or print any error that occurs during file operation
        print(f"Error saving metadata: {e}")