import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://www.bris.ac.uk/where-is-my/find/study-desk/table"
OUTPUT_FILE = "seat_availability.csv"

def scrape_seat_data():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to retrieve page")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    
    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            location = cols[0].text.strip()
            free_seats = cols[1].text.strip()
            data.append([timestamp, location, free_seats])
    
    df = pd.DataFrame(data, columns=["Timestamp", "Location", "Seats Free"])
    
    try:
        existing_df = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass  # If file doesn't exist, create it fresh
    
    df.to_csv(OUTPUT_FILE, index=False)
    print("Data saved successfully.")

if __name__ == "__main__":
    scrape_seat_data()
