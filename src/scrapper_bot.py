from src.base_web_bot import WebBot
from selenium.webdriver.common.by import By
from datetime import datetime
from typing import Dict, List

class ScrapperBot(WebBot):
    """
    A specialized bot for scraping available resources from a booking page.

    Inherits from WebBot and adds functionality specific to scraping available resources and timeslots.

    Attributes:
        resource_schedule (Dict[str, List[datetime]]): A dictionary mapping resource names to lists of datetime objects representing their available times.

    Methods:
        __init__(self, username, password, login_url): Initializes the ScrapperBot with user credentials and login URL.
        get_available_resources(self): Retrieves available resources from the booking page and formats them using parse_slots_to_resource_schedule.
        parse_slots_to_resource_schedule(self, slots): Parses slot information into a structured resource schedule.
        filter_resources_by_time(self, start_datetime, end_datetime): Filters resources that are available throughout a specified time range.
    """

    def __init__(self, username: str, password: str, login_url: str) -> None:
        """
        Initializes the ScrapperBot with user credentials and login URL.

        ### Args:
            username: The username for login.
            password: The password for login.
            login_url: The URL of the login page.

        ### Returns:
            None
        """
        super().__init__(username, password, login_url)
        self.resource_schedule: Dict[str, List[datetime]] = {}

    def get_available_resources(self) -> Dict[str, List[datetime]]:
        """
        Retrieves available resources from the web page and formats them.

        ### Returns:
            A dictionary mapping resource names to lists of datetime objects representing their available times.
        """
        available_slots = self.driver.find_elements(
            By.XPATH, "//a[contains(@class, 'fc-timeline-event') and contains(@title, 'Available')]"
        )
        all_slots = [slot.get_attribute("title") for slot in available_slots]
        self.resource_schedule = self.parse_slots_to_resource_schedule(all_slots)
        return self.resource_schedule
    
    def parse_slots_to_resource_schedule(self, slots: List[str]) -> Dict[str, List[datetime]]:
        """
        Parses slot information into a structured resource schedule.

        ### Args:
            slots: A list of strings representing available slots.

        ### Returns:
            A dictionary mapping resource names to lists of datetime objects representing their scheduled times.
        """
        resource_schedule = {}
        datetime_format = "%I:%M%p %A, %B %d, %Y"

        for slot in slots:
            time_slot_str, resource_name = slot.split(" - ")[:2]
            timeslot = datetime.strptime(time_slot_str, datetime_format)
            resource_schedule.setdefault(resource_name, []).append(timeslot)

        return resource_schedule
    
    def filter_resources_by_time(self, start_datetime: datetime, end_datetime: datetime) -> List[str]:
        """
        Filters resources that are available throughout a specified time range,
        assuming resources are scheduled in 15-minute intervals.

        ### Args:
            start_datetime: The start of the desired time range.
            end_datetime: The end of the desired time range.

        ### Returns:
            A list of resource names available throughout the specified time range.
        """
        available_resources = [
            resource_name
            for resource_name, available_times in self.resource_schedule.items()
            if any(start_datetime <= timeslot <= end_datetime for timeslot in available_times)
        ]
        return available_resources