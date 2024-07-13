from src.base_web_bot import WebBot
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.utils import save_screenshot
from datetime import datetime

# booking_bot.py
class BookingBot(WebBot):
    """
    A bot designed for automating the booking of resources on a web page.

    Inherits from WebBot and adds functionality for submitting bookings for available resources.

    Attributes:
        output_folder (str): The folder path where screenshots of successful bookings are saved.

    Methods:
        __init__(self, username, password, login_url, wait_time=5): Initializes the BookingBot with user credentials, login URL, and default wait time.
        submit_booking(self, resource_timeslot): Submits a booking for a given resource timeslot.
        book_resource_by_time(self, start_datetime, resource_name): Books a resource based on a specific start datetime and resource name.
        book_earliest_resource_category(self, resource_category): Books the earliest available timeslot for a given resource category.
    """

    def __init__(self, username: str, password: str, login_url: str, wait_time: int = 5) -> None:
        super().__init__(username, password, login_url, wait_time)
        self.output_folder = "bookings"

    def submit_booking(self, resource_timeslot: webdriver.remote.webelement.WebElement) -> bool:
        """
        Submits a booking for the selected timeslot and waits for a confirmation message.

        ### Args:
            timeslot: The WebElement representing the timeslot for a particular resource to book.
        
        ### Returns:
            A boolean indicating whether the booking was successful.
        """
        self.driver.execute_script("arguments[0].click();", resource_timeslot)
        self.click_button("submit_times")
        self.click_button("terms_accept")
        self.click_button("btn-form-submit")
        
        # Wait for the confirmation message
        success_confirmation_message = self.wait_for_element(By.XPATH, "//*[contains(text(), 'successfully booked')]", timeout=10)
        if success_confirmation_message:
            save_screenshot(self.driver, self.output_folder, self.username)
            return True
        else:
            return False
        

    def book_resource_by_time(self, start_datetime: datetime, resource_name: str) -> None:
        """
        Books an individual slot based on the specified start datetime and resource name.

        ### Args:
            start_datetime: The start datetime of the slot to book.
            resource_name: The name of the resource to book.

        ### Returns:
            A boolean indicating whether the booking was successful.
        """
        resource_timeslot_str = f"{start_datetime.strftime("%-I:%M%p %A, %B %d, %Y").lower()} - {resource_name} - Available"
        resource_timeslot = self.wait_for_element(By.XPATH, f"//a[contains(@class, 'fc-timeline-event') and contains(@title, '{resource_timeslot_str}')]")
        if resource_timeslot:
            booking_status = self.submit_booking(resource_timeslot)

        return booking_status

    def book_earliest_resource_category(self, resource_category: str) -> None:
        """
        Books the earliest available slot for the specified resource.

        ### Args:
            resource_name: The category of the resource for which to book the earliest available slot.

        ### Returns:
            A boolean indicating whether the booking was successful.
        """
        timeslot = self.wait_for_element(By.XPATH, f"//a[contains(@class, 'fc-timeline-event') and contains(@title, 'Available') and contains(@title, '{resource_category}')]")
        if timeslot:
            booking_status =self.submit_booking(timeslot)
        return booking_status