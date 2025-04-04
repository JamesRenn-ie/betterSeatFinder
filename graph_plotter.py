import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Load the data from the CSV file
file_path = 'seat_availability.csv'
data = pd.read_csv(file_path)

# Remove rows where 'Seats Free' contains '??'
data = data[data['Seats Free'] != '??']

# Convert the 'Timestamp' column to datetime objects
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Convert 'Seats Free' column to numeric (just in case there are any other non-numeric values)
data['Seats Free'] = pd.to_numeric(data['Seats Free'], errors='coerce')

# Drop rows where 'Seats Free' could not be converted (i.e., still NaN)
data = data.dropna(subset=['Seats Free'])

# Extract only the time part of the timestamp for plotting
data['Time'] = data['Timestamp'].dt.strftime('%H:%M:%S')

# Get unique locations
locations = data['Location'].unique()

# Create a directory to save the plots
output_dir = 'seat_availability_plots'
os.makedirs(output_dir, exist_ok=True)

# Plotting for each location
for location in locations:
    # Filter data for the current location
    location_data = data[data['Location'] == location]
    
    # Group the data by 'Time' and compute the mean 'Seats Free' for each time point
    time_grouped = location_data.groupby('Time')['Seats Free'].mean().reset_index()
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(time_grouped['Time'], time_grouped['Seats Free'], marker='o', linestyle='-')
    plt.title(f'Total Seats Free Over Time - {location}')
    plt.xlabel('Time of Day')
    plt.ylabel('Total Seats Free')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot as a PNG file
    safe_location_name = location.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')
    plt.savefig(os.path.join(output_dir, f'{safe_location_name}.png'))
    plt.close()

print(f"Plots saved in the directory: {output_dir}")
