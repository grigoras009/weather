import requests
import csv

from datetime import datetime, timedelta


def get_monthly_date_ranges(year):
    """
    Generate start and end dates for each month in the given year.

    :param year: The year for which to generate monthly date ranges.
    :return: A list of (start_date, end_date) tuples as strings in 'YYYY-MM-DD' format.
    """
    date_ranges = []
    for month in range(1, 11):  # Loop through months 1 to 12
        # Start of the month
        start_date = datetime(year, month, 1)
        # End of the month (handle varying days in month)
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        # Add range as strings
        date_ranges.append((start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    return date_ranges

print(get_monthly_date_ranges(2024))

def fetch_weather_data(api_key, location, year):
    """
    Fetch weather data for each month of the given year.

    :param api_key: Your WeatherAPI key.
    :param location: The location to query weather for.
    :param year: The year for which to fetch weather data.
    :return: A list of responses for each month.
    """
    date_ranges = get_monthly_date_ranges(year)
    all_responses = []

    for start_date, end_date in date_ranges:
        # Define the API endpoint and parameters
        url = "https://api.weatherapi.com/v1/history.json"
        params = {
            "key": api_key,
            "q": location,
            "dt": start_date,
            "end_dt": end_date
        }

        try:
            # Make the GET request
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            all_responses.append(response.json())  # Append JSON data
            print(f"Fetched data for {start_date} to {end_date}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {start_date} to {end_date}: {e}")
    print(all_responses)
    return all_responses

#Example usage
api_key = "289c8e8bad9b44bfa60172634241611"
location = "Bangkok"
year_to_query = 2024
weather_data = fetch_weather_data(api_key, location, year_to_query)

csv_file = "weather_data.csv"
# Loop through weather data responses (one for each month)
for monthly_data in weather_data:
    location = monthly_data['location']['name']
    forecast_days = monthly_data['forecast']['forecastday']  # A list of daily forecast data for this month

    # Open CSV file and write headers and rows
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write data rows for each day in this month's forecast
        for day in forecast_days:
            writer.writerow([
                day['date'],
                location,
                day['day']['maxtemp_c'],
                day['day']['mintemp_c'],
                day['day']['avgtemp_c'],
                day['day']['maxwind_kph'],
                day['day']['totalprecip_mm'],
                day['day']['avghumidity'],
                day['day']['daily_chance_of_rain'],
                day['day']['daily_chance_of_snow'],
                day['day']['condition']['text'],
                day['astro']['sunrise'],
                day['astro']['sunset'],
            ])

