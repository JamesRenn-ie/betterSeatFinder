import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
file_path = 'seat_availability.csv'
data = pd.read_csv(file_path)

# Remove invalid 'Seats Free' entries
data = data[data['Seats Free'] != '??']
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['Seats Free'] = pd.to_numeric(data['Seats Free'], errors='coerce')
data = data.dropna(subset=['Seats Free'])

# Sort and remove consecutive identical measurements per location
data = data.sort_values(by=['Location', 'Timestamp'])
data = data[data['Seats Free'].ne(data.groupby('Location')['Seats Free'].shift())]

# Extract hour and day of week
data['Hour'] = data['Timestamp'].dt.hour
data['Day Name'] = data['Timestamp'].dt.day_name()

# Limit data to hours between 6 AM and midnight
data = data[(data['Hour'] >= 6) & (data['Hour'] <= 23)]

# Get all unique locations and weekday names
locations = data['Location'].unique()
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Set the desired hour range for x-axis
hour_range = list(range(6, 24))

# Create output directory
output_dir = 'seat_availability_plots'
os.makedirs(output_dir, exist_ok=True)

# Plot for each location
for location in locations:
    location_data = data[data['Location'] == location]
    
    plt.figure(figsize=(12, 6))

    for day in weekdays:
        day_data = location_data[location_data['Day Name'] == day]
        hour_grouped = day_data.groupby('Hour')['Seats Free'].mean().reset_index()
        plt.plot(hour_grouped['Hour'], hour_grouped['Seats Free'], label=day, marker='o')

    plt.title(f'Seats Free by Hour and Day - {location}')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Seats Free')
    plt.xticks(hour_range)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    safe_location_name = location.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')
    plt.savefig(os.path.join(output_dir, f'{safe_location_name}_by_day.png'))
    plt.close()

print(f"Updated plots saved in {output_dir}")
