import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
from datetime import timedelta

# Setup argument parser
parser = argparse.ArgumentParser(description='Generate seat availability plots.')
parser.add_argument('--last-two-weeks', action='store_true', help='Limit data to the last two weeks only.')
args = parser.parse_args()

# Load the data
file_path = 'seat_availability.csv'
data = pd.read_csv(file_path)

# Remove invalid 'Seats Free' entries
data = data[data['Seats Free'] != '??']
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['Seats Free'] = pd.to_numeric(data['Seats Free'], errors='coerce')
data = data.dropna(subset=['Seats Free'])

# Filter to last 2 weeks if argument is passed
if args.last_two_weeks:
    end_date = data['Timestamp'].max()
    start_date = end_date - timedelta(weeks=2)
    data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
    date_suffix = f"{start_date.date()}_to_{end_date.date()}"
    output_dir = f'seat_availability_plots_last_2_weeks_{date_suffix}'
else:
    output_dir = 'seat_availability_plots'

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
hour_range = list(range(6, 24))

# Create output directory
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
    filename = f'{safe_location_name}_by_day'
    if args.last_two_weeks:
        filename += f'_{date_suffix}'
    filename += '.png'

    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

print(f"Plots saved in '{output_dir}'")
