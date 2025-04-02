import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# URL of the study spaces page
URL = "https://www.bris.ac.uk/where-is-my/find/study-desk/table"
OUTPUT_FILE = "seat_availability.csv"

def scrape_seat_data():
    # Set up Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.headless = False  # Set to True to run without opening a browser window
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    time.sleep(10)  # Allow time for JavaScript to load content

    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Find all sections containing study space data
        study_spaces = driver.find_elements(By.CLASS_NAME, "row.align-items-center")

        for space in study_spaces:
            try:
                # Extract location name
                location_elem = space.find_element(By.TAG_NAME, "a")
                location = location_elem.text.strip()

                # Extract available seats
                seats_available_elem = space.find_element(By.CLASS_NAME, "space-available")
                seats_available = seats_available_elem.text.strip()

                # Extract total seats (removing 'of X available' text)
                seats_total_elem = space.find_element(By.CLASS_NAME, "space-total")
                seats_total = seats_total_elem.text.split()[1]  # Get the number after 'of'

                data.append([timestamp, location, seats_available, seats_total])

            except Exception as e:
                print(f"Error extracting data for a study space: {e}")

    except Exception as e:
        print(f"Error extracting data: {e}")

    finally:
        driver.quit()

    # Save to CSV
    df = pd.DataFrame(data, columns=["Timestamp", "Location", "Seats Free", "Total Seats"])
    
    try:
        existing_df = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass  # If file doesn't exist, create it fresh

    df.to_csv(OUTPUT_FILE, index=False)
    print("Data saved successfully.")

if __name__ == "__main__":
    scrape_seat_data()
