# Library Booker Bot
A simple Selenium bot project designed to automate the booking of university library resources.

## Project Motivation
When I couldn't secure student lodging, studying became nearly impossible at home, where I lacked a private room. Unable to find space even in a friend's cramped dorm, I resorted to daily trips to the library since I didn't want my grades to suffer. Booking a study slot with a monitor was tough due to strict rules. Frustrated with others snatching away my much-needed monitor (a essential for a CS student), I developed an automated booking solution using Selenium with multiple accounts and deployed it on Heroku.

Was it fair to other students? No. Did it teach me a lot about Selenium and OOP? Yes. Did it save my grades? Not really, no. But it was fun.

## Project Structure
```
├── Procfile # Specifies commands to be executed by the application on startup.
├── README.md # This file provides project documentation.
├── bookings # Directory for storing booking logs or data (if applicable).
├── conf # Configuration file to manage bot settings like credentials, URLs and booking resource information.
│   └── config.yaml
├── main.py # Entry point of the application. Initializes and runs the bots.
├── requirements.txt
└── src
    ├── __init__.py
    ├── base_web_bot.py # Base class for creating web bots, providing common functionalities.
    ├── booking_bot.py # Implements the specific logic for booking resources. 
    ├── scrapper_bot.py # Contains logic for scraping web pages to find available resources. 
    └── utils.py # Utility functions used across the project, e.g., initializtion of drivers and logging of booking metadata.
```

## Installation Steps

1. **Clone the Repository**
   - Clone this repository to your local machine using `git clone <repository-url>`.

2. **Set Up a Virtual Environment** (Optional but recommended)
   - Navigate to the project directory: `cd ntu_library_booker`
   - Create a virtual environment: `python3 -m venv venv`
   - Activate the virtual environment:
     - On Windows: `.\venv\Scripts\activate`
     - On Unix or MacOS: `source venv/bin/activate`

3. **Install Dependencies**
   - Ensure you are in the project root directory where `requirements.txt` is located.
   - Install the required Python packages: `pip install -r requirements.txt`

4. **Configure the Application**
- Navigate to the `conf` directory.
- Edit `config.yaml` to set up your preferences for the booking bot. Here is the structure of the `config.yaml` file:

```yaml
login_url: "https:myspace.com"
location: "XX XX Library"
resource_category: "XX Resource Type"
preferred_resource_id: "XX XX"
times:
  start: "0800"  # Start time as a string in 24-hour format
  end: "1800"    # End time as a string in 24-hour format
output_folder: "bookings"
```

Create a .env file in the root directory of your project to store sensitive information such as credentials. This file should NOT be committed to version control. Add the following lines to your .env file, replacing your_username and your_password with your actual login credentials:

```CREDENTIALS={"username": "password", "username2": "password2", ...}```

5. **Running the Application**
   *Local* - From the project root directory, run `python main.py` to start the bot.

## Classes and Modules

- `**WebBot**`: This class serves as a foundation for any web bot, providing common functionalities such as initiating a web driver, navigating pages, and handling web elements.
  
- `**ScrapperBot**`: Also extends `WebBot`, focused on scraping web pages to gather information about available resources, which can then be used by `BookingBot`.

- `**BookingBot**`: Extends `WebBot` to implement the booking process. It includes methods for logging in to websites, finding available resources, and completing the booking process.

- **utils.py**: Contains utility functions that support the bots' operations, including initializtion of drivers and logging of booking metadata.

## Future Work
1. Conduct another round of testing with Heroku.
2. Dockerize it. 
3. Implement functionality to retrieve confirmation codes from emails and input them directly to secure the booking slot (currently limited by Azure authentication protocols).
4. Send confirmation/summary of booked resources to Gmail.
5. Integrate a Telegram bot to enhance the ability to select and filter resources.
