#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 19:39:12 2023

@author: francesc
"""


# Send a request to the URL and get the HTML content
url1 = "https://www.meteosantfeliu.cat/WXDailyHistory.php?ID=ICTSANTF2&month=07&day=18&year=2023&format=1&graphspan=day"

response = requests.get(url1)
html_content = response.content

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

data=soup.get_text()
# Convert the data to a list of lists
rows = [line.split(',') for line in data.strip().split('\n')]


# Convert the list of lists to a pandas DataFrame
df1 = pd.DataFrame(rows, columns=['Time', 'TemperatureC', 'DewpointC', 'PressurehPa', 'WindDirection', 'WindDirectionDegrees', 'WindSpeedKMH', 'WindSpeedGustKMH', 'Humidity', 'HourlyPrecipMM', 'Conditions', 'Clouds', 'dailyrainMM', 'SolarRadiationWatts/m^2', 'UVIndex', 'SoftwareType', 'DateUTC'])

# Filter out rows with 'DateUTC' in the 'DateUTC' column
df1 = df1[df1['DateUTC'] != 'DateUTC']

# Convert the "DateUTC" column to datetime data type
df1['DateUTC'] = pd.to_datetime(df1['DateUTC'], format='%Y-%m-%dT%H:%M:%SZ')

# Convert the "Time" column to datetime data type
df1['Time'] = pd.to_datetime(df1['Time'])

# Set the "Time" column as the DataFrame index
df1.set_index('Time', inplace=True)

# Drop the "DateUTC" column as it's no longer needed in the index
df1.drop(columns='DateUTC', inplace=True)

# Drop rows with 'None' values in the DataFrame
df1 = df1.dropna()

# Display the DataFrame
print(df1)

# Convert the "TemperatureC" column to numeric (float) data type
df1['TemperatureC'] = pd.to_numeric(df1['TemperatureC'], errors='coerce')
df1['WindDirectionDegrees'] = pd.to_numeric(df1['WindDirectionDegrees'], errors='coerce')
df1['Humidity'] = pd.to_numeric(df1['Humidity'], errors='coerce')


################ plot
import matplotlib.pyplot as plt
import numpy as np

def deg_to_compass(degrees):
    val = int((degrees / 22.5) + 0.5)
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return directions[(val % 16)]

df.Temperature = pd.to_numeric(df.TemperatureC, errors='coerce')


# Plot the "TemperatureC" data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df.Temperature, color='blue', label='Temperature (°C)')
plt.xlabel('Time')
plt.ylabel('Temperatura (°C)')
plt.ylim(min(df.Temperature), max(df.Temperature+1))  # Set the y-axis range from 20 to 45
plt.title('28 de juny del 2019')
plt.grid(True)
# Find the maximum value and its corresponding time index
max_value = df.Temperature.max()
max_index = df.Temperature.idxmax()

# Annotate the maximum value on the graph
plt.text(max_index, max_value, f'Max: {max_value:.2f} °C', ha='right', va='bottom')

# Create a second y-axis for wind direction data
ax2 = plt.twinx()
ax2.plot(df.index, df['WindDirectionDegrees'], color='green', label='Wind Direction (°)')
ax2.set_ylim(0, 360)  # Set the y-axis range for wind direction
ax2.set_ylabel('Wind Direction (°)')

# Convert the y-axis tick labels from degrees to compass directions
ax2.set_yticks(np.arange(0, 360, 45))
ax2.set_yticklabels([deg_to_compass(deg) for deg in np.arange(0, 360, 45)])

max_temp = df.Temperature.max()
max_time = df.Temperature.idxmax()

lines, labels = plt.gca().get_legend_handles_labels()
#lines2, labels2 = plt.get_legend_handles_labels()
plt.legend(lines, labels , loc='upper left')
plt.scatter(max_time, max_temp+305, color='red', label=f'Max Temp: {max_temp:.2f} °C')

# Add faint bars for humidity data
ax3 = ax2.twinx()
ax3.bar(df.index, df['Humidity'], color='gray', alpha=0.3, width=0.005, align='center', label='Humidity')
ax3.set_ylim(0, 100)  # Set the y-axis range for humidity
ax3.set_ylabel('Humidity (%)')

plt.show()


#####################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def deg_to_compass(degrees):
    val = int((degrees / 22.5) + 0.5)
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return directions[(val % 16)]

# Assuming df is the DataFrame with the data
df1.Temperature = pd.to_numeric(df1.TemperatureC, errors='coerce')

# Plot the "TemperatureC" data
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.plot(df.index, df.TemperatureC, color='blue')#, label='Temperature (°C)')
ax1.plot(df.index[:len(df1.Temperature)], df1.TemperatureC, color='red')#, label='Temperature (°C)')

ax1.set_xlabel('Temps')
ax1.set_ylabel('Temperatura (°C)')
ax1.set_ylim(min(df.TemperatureC), max(df.TemperatureC+1))  # Set the y-axis range from 20 to 45
ax1.set_title('28 de juny del 2019')
ax1.grid(True)

# Find the maximum value and its corresponding time index
max_value = df.TemperatureC.max()
max_index = df.TemperatureC.idxmax()

# Annotate the maximum value on the graph
ax1.scatter(max_index, max_value, color='red', label=f'Max Temp: {max_value:.2f} °C')
ax1.annotate(f'{max_value:.2f} °C', xy=(max_index, max_value), xytext=(max_index - pd.Timedelta(hours=1), max_value + 1), color='red',
             arrowprops=dict(arrowstyle="->", color='red'), ha='left', va='top')

# Plot the wind direction data
ax2.plot(df.index, df['WindDirectionDegrees'], color='green', label='Wind Direction (°)')
ax2.set_ylim(0, 360)  # Set the y-axis range for wind direction
ax2.set_ylabel('\n\nDirecció del vent')

# Convert the y-axis tick labels from degrees to compass directions
ax2.set_yticks(np.arange(0, 360, 45))
ax2.set_yticklabels([deg_to_compass(deg) for deg in np.arange(0, 360, 45)])

# Add faint bars for humidity data
ax3 = ax1.twinx()
ax3.bar(df.index, df['Humidity'], color='gray', alpha=0.3, width=0.005, align='center')
ax3.set_ylim(0, 100)  # Set the y-axis range for humidity
ax3.set_ylabel('Humitat relativa (%)')

# Annotate the maximum humidity value on the graph
max_humidity = df['Humidity'].max()
max_time = df['Humidity'].idxmax()
ax3.scatter(max_time, max_humidity, color='blue', label=f'HR màxima: {max_humidity:.2f}%')
#ax3.annotate(f'Max Humidity: {max_humidity:.2f}%', xy=(max_time, max_humidity), xytext=(max_time + pd.Timedelta(hours=1), max_humidity + 5), color='blue',
#             arrowprops=dict(arrowstyle="->", color='blue'), ha='left', va='bottom')

#ax4 = ax1.twinx()
#ax4.plot(df.index[:len(df1.Temperature)], df1.TemperatureC, color='red')#, label='Temperature (°C)')
#ax4.set_xlabel('Temps')
#ax4.set_ylabel('Temperatura (°C)')
#ax4.set_title('28 de juny del 2019')
#ax4.grid(True)

plt.legend(loc='upper left')
plt.show()
