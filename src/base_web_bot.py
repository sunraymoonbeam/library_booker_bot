from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from src.utils import initialize_driver
from typing import Optional, Callable

class WebBot:
    """
    A base class for creating web bots using Selenium for automating web interactions.

    Attributes:
        driver (webdriver): The Selenium WebDriver instance for browser automation.
        username (str): The username for login.
        password (str): The password for login.
        login_url (str): The URL of the login page.
        default_wait_time (int): The default time to wait for elements to appear on the page.

    Methods:
        __init__(self, username, password, login_url, wait_time=5): Initializes the WebBot with user credentials, login URL, and default wait time.
        wait_for_element(self, by, value, timeout=None, condition=EC.presence_of_element_located): Waits for a web element to be present on the page and returns it.
        login(self): Logs into the website using the provided credentials.
        navigate_to_booking_page(self, location, resource_category): Navigates to the booking page by selecting the specified location and resource category.
        select_option(self, element_id, option): Selects an option from a dropdown menu.
        click_button(self, element_id): Clicks a button identified by its element ID.
        close_driver(self): Closes the Selenium WebDriver and exits the browser.
    """

    def __init__(self, username: str, password: str, login_url: str, wait_time: int = 5) -> None:
        """
        Initializes the web bot with user credentials and the login URL.

        ### Args:
            username: The username for login.
            password: The password for login.
            login_url: The URL of the login page.
            wait_time: The default time to wait for elements to appear.

        ### Returns:
            None
        """
        self.driver = initialize_driver()
        self.username = username
        self.password = password
        self.login_url = login_url
        self.default_wait_time = wait_time

    def wait_for_element(self, by: By, value: str, timeout: int = None, condition: Callable = EC.presence_of_element_located) -> Optional[webdriver.remote.webelement.WebElement]:
        """
        Waits for an element to be present on the page and returns it.

        ### Args:
            by: The type of strategy to locate the element.
            value: The value of the locator strategy.
            timeout: The time to wait before timing out.
            condition: The condition to wait for.

        ### Returns:
            The WebElement if found, None otherwise.
        """
        try:
            element = WebDriverWait(self.driver, self.default_wait_time if timeout is None else timeout).until(condition((by, value)))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element by {by} with value {value}")
        except NoSuchElementException:
            print(f"Element by {by} with value {value} was not found on the page")
        return None

    def login(self) -> None:
        """
        Logs into the website using the provided credentials.
        """
        self.driver.get(self.login_url)
        username_field = self.wait_for_element(By.ID, "userNameInput")
        password_field = self.wait_for_element(By.ID, "passwordInput")

        if username_field and password_field:
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

    def navigate_to_booking_page(self, location: str, resource_category: str) -> None:
        """
        Navigates to the booking page by selecting the specified location and resource category.
        
        ### Args:
            location: The location to select. e.g. Business Library, Chinese Library, etc.
            resource_category: The resource category to select. e.g. Discussion Pod, PC / Monitor, etc.

        ### Returns:
            None
        """
        self.select_option("lid", location)
        self.select_option("gid", resource_category)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll to the bottom of the page for better visibility for user

    def select_option(self, element_id: str, option: str) -> None:
        """
        Selects an option from a dropdown menu.

        ### Args:
            element_id: The ID of the select element.
            option: The visible text of the option to select.

        ### Returns:
            None
        """
        select_element = Select(self.wait_for_element(By.ID, element_id))
        if select_element:
            select_element.select_by_visible_text(option)

    def click_button(self, element_id: str) -> None:
        """
        Clicks a button identified by its element ID.

        ### Args:
            element_id: The ID of the button to click.

        ### Returns:
            None
        """
        button_element = self.wait_for_element(By.ID, element_id)
        if button_element:
            button_element.click()

    def close_driver(self) -> None:
        """
        Closes the Selenium WebDriver and exits the browser.
        """
        self.driver.quit()