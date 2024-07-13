import os
import hydra
from dotenv import load_dotenv
from omegaconf import DictConfig
from src.booking_bot import BookingBot
from src.scrapper_bot import ScrapperBot
from src.utils import convert_str_datetime
from datetime import timedelta
import json

# Load environment variables
load_dotenv(dotenv_path= "conf/.env")

@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig):
    # Parse credentials from .env file
    credentials = json.loads(os.getenv("CREDENTIALS"))

    login_url = cfg.login_url
    location = cfg.location 
    resource_category = cfg.resource_category  # Type of resource (PC, monitor, etc.)
    preferred_resource_id = cfg.preferred_resource_id  # Specific name of the resource
    start_slot_time = convert_str_datetime(cfg.times.start)
    end_slot_time = convert_str_datetime(cfg.times.end)
    
    # Initialize ScrapperBot to find available resources
    scrapper = ScrapperBot(username=list(credentials.keys())[0],  # Use the first user for scraping
                           password=list(credentials.values())[0],
                           login_url=login_url)
    scrapper.login()
    scrapper.navigate_to_booking_page(location, resource_category)
    scrapper.get_available_resources()
    available_resources = scrapper.filter_resources_by_time(start_slot_time, end_slot_time)
    scrapper.close_driver()
    
    if available_resources:
        print("Available resources:")
        for i, resource in enumerate(available_resources):
            print(f"{i + 1}. {resource}")
        
        # Determine the resource to book
        if preferred_resource_id in available_resources:
            selected_resource = preferred_resource_id
            print(f"Preferred resource {preferred_resource_id} is available.")
        else:
            selected_resource = available_resources[0]  # Take the first valid resource
            print(f"Preferred resource {preferred_resource_id} is NOT available - booking {selected_resource} instead.")
        
        current_slot_time = start_slot_time
        # Booking process for each user
        for username, password in credentials.items():
            if current_slot_time >= end_slot_time:
                print("Booking window closed.")
                break
            
            print(f"Booking {selected_resource} for {username} for timeslot {current_slot_time}.")
            booker = BookingBot(username=username, 
                                password=password,
                                login_url=login_url,
                                output_folder=cfg.output_folder)
            booker.login()
            booker.navigate_to_booking_page(location, resource_category)
            booking_confirmation = booker.book_resource_by_time(selected_resource, current_slot_time)
            if booking_confirmation:
                print(f"Booking successful for {username}.")
                booker.save_metadata(cfg.output_folder, username, current_slot_time, end_slot_time, location, resource_category, selected_resource)
            else:
                print(f"Booking failed for {username}.")
            booker.close_driver()
            start_slot_time += timedelta(hours=2)  # Increment booking time by 2 hours
    else:
        print("No available resources in the specified time range.")

if __name__ == "__main__":
    main()