import pandas as pd
import os
import json

# Load the data
file_path = 'seat_availability.csv'
data = pd.read_csv(file_path)

# Clean and convert
data = data[data['Seats Free'] != '??']
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['Seats Free'] = pd.to_numeric(data['Seats Free'], errors='coerce')
data = data.dropna(subset=['Seats Free'])

# Sort and remove consecutive identical values per location
data = data.sort_values(by=['Location', 'Timestamp'])
data = data[data['Seats Free'].ne(data.groupby('Location')['Seats Free'].shift())]

# Extract hour and weekday
data['Hour'] = data['Timestamp'].dt.hour
data['Day Name'] = data['Timestamp'].dt.day_name()

# Filter to hours between 6am and midnight
data = data[(data['Hour'] >= 6) & (data['Hour'] <= 23)]

# Days of the week in order
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Group and prepare JSON structure
output = {}
locations = data['Location'].unique()

for location in locations:
    loc_data = data[data['Location'] == location]
    location_dict = {}
    
    for day in weekdays:
        day_data = loc_data[loc_data['Day Name'] == day]
        hourly = day_data.groupby('Hour')['Seats Free'].mean()
        full_hours = pd.Series(index=range(6, 24), data=0.0)
        full_hours.update(hourly)
        location_dict[day] = [round(v, 2) for v in full_hours.tolist()]
    
    output[location] = location_dict

# Write to JSON
os.makedirs("output", exist_ok=True)
with open("output/seat_busyness.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Busyness data exported to output/seat_busyness.json")
