import requests
import argparse
import pandas as pd

def fetch_data(year, month):
    # Ensure inputs are properly formatted
    month = f"{int(month):02d}"
    year = f"{int(year):02d}"

    # Construct the URL
    url = f"https://data.meteosantfeliu.cat/meteo/reports/noaa/NOAAMO{month}{year}.txt"
    print(url)

    # Send a request to get the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve data from {url}. Status code: {response.status_code}")
        return

    content = response.text

    # Split the content into lines
    lines = content.splitlines()

    # Find the line number containing the delimiter
    delimiter = '----------------------------------------------------------------------------------'
    line_number = None
    for idx, line in enumerate(lines):
        if delimiter in line:
            line_number = idx
            break

    if line_number is None:
        print("The delimiter was not found in the lines.")
        return

    # Start processing data from the next line after the delimiter
    line_number += 1

    # Determine the number of days in the month
    if int(month) in [1, 3, 5, 7, 8, 10, 12]:
        number_of_days = 31
    elif int(month) in [4, 6, 9, 11]:
        number_of_days = 30
    else:
        number_of_days = 29 if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0) else 28

    line_number_final = line_number + number_of_days

    # Extract data and keep relevant columns
    daily_data = []
    for line in lines[line_number:line_number_final]:
        parts = line.split()
        if len(parts) >= 13:  # Ensure the line has enough columns
            day = parts[0]
            temp_mean = parts[1]
            temp_high = parts[2]
            high_time = parts[3]
            temp_low = parts[4]
            low_time = parts[5]
            heat_deg_days = parts[6]
            cool_deg_days = parts[7]
            rain = parts[8]
            wind_speed = parts[9]
            high_wind = parts[10]
            high_wind_time = parts[11]
            dom_dir = parts[12]
            daily_data.append([
                day, temp_mean, temp_high, high_time, temp_low, low_time,
                heat_deg_days, cool_deg_days, rain, wind_speed,
                high_wind, high_wind_time, dom_dir
            ])

    # Create a DataFrame
    columns = [
        "Day", "Mean Temp", "High Temp", "High Time", "Low Temp", "Low Time",
        "Heat Deg Days", "Cool Deg Days", "Rain (mm)", "Avg Wind Speed (km/h)",
        "High Wind", "High Wind Time", "Dom Dir"
    ]
    df = pd.DataFrame(daily_data, columns=columns)

    # Display the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    filename = f"{year}{month}.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Fetch weather data for a specific year and month.")
    parser.add_argument("year", type=str, help="Year (e.g., 2023)")
    parser.add_argument("month", type=int, choices=range(1, 13), help="Month (1-12)")

    # Parse the arguments
    args = parser.parse_args()

    # Call the fetch_data function with the parsed arguments
    fetch_data(args.year, args.month)

if __name__ == "__main__":
    main()

