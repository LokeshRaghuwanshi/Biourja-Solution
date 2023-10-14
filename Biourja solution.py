import pandas as pd
import numpy as np

# Constants and input data
total_wind_farms = 100
zones = {'E': 24, 'N': 26, 'W': 15, 'S': 35}
zonal_forecasts = {'E': 2800, 'W': 1500, 'N': 2000, 'S': 6500}
state_forecast = 12000
input_data_file = "C:\\Users\\LOKESH\\Downloads\\biourja-efzrr-y7i38ed9-input.csv"

# Load input data
data = pd.read_csv(input_data_file)

# Extract zone information from 'Plant_Name'
data['Zone'] = data['Plant_Name'].apply(lambda x: x[0])

# Calculate individual ratios and zonal ratios
data['individual_ratio'] = data['Forecast'] / data['Capacity']
data['zone_forecast'] = data['Zone'].apply(lambda zone: zonal_forecasts[zone])

# Calculate the redistribution factor for each wind farm
data['redistribution_factor'] = data['individual_ratio'] * (data['zone_forecast'] / data['Forecast'].sum())

# Ensure redistribution factor doesn't exceed 1
data['redistribution_factor'] = np.minimum(data['redistribution_factor'], 1)

# Calculate the redistributed dispatch for each wind farm
data['Forecast'] = data['redistribution_factor'] * state_forecast

# Ensure dispatch doesn't exceed capacity
data['Forecast'] = np.minimum(data['Forecast'], data['Capacity'])

# Calculate the sum of redistributed dispatch for each zone
zone_dispatch_sum = data.groupby('Zone')['Forecast'].sum()

# Normalize the redistributed dispatch for each zone based on the total forecast
data['Forecast'] = data.apply(lambda row: row['Forecast'] / zone_dispatch_sum[row['Zone']] * zonal_forecasts[row['Zone']], axis=1)

# Ensure dispatch doesn't exceed capacity after normalization
data['Forecast'] = np.minimum(data['Forecast'], data['Capacity'])

# Adjust the forecast values to ensure the total sum is not exceeding 1200
total_forecast = data['Forecast'].sum()
if total_forecast > state_forecast:
    # Scale down the forecasts to match the state forecast
    data['Forecast'] *= state_forecast / total_forecast




# Print the final redistributed dispatch for each wind farm in CSV format
print(data[['Plant_Name', 'Forecast']].to_csv(index=False))