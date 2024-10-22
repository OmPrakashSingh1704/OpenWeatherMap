import datetime
import pyowm
import os
from .LLMsummary import send_warning, send_summary
from .report_db import addSummary
from .weather_db import addWeather, shouldUpdateWeather, dropDataBefore24Hours, Warning, Summary


# Function to call the OpenWeatherMap API for the specified city
def owm_api_call(city):
    """
    Call the OpenWeatherMap API for the specified city and retrieve the
    current weather data.

    Parameters
    ----------
    city : str
        The city for which to retrieve the weather data.

    Returns
    -------
    observation : pyowm.weatherapi25.weather_manager.WeatherManager
        The pyowm observation object containing the current weather data.

    """
    # Create an instance of the OpenWeatherMap API
    owm = pyowm.OWM(os.getenv("OPENWEATHER_API_KEY"))

    # Retrieve the current weather for the specified city
    observation = owm.weather_manager().weather_at_place(city)

    # Return the observation object
    return observation


# Function to get the weather for a specific city and store it in the database
def getWeather(city):
    """
    Retrieves the current weather for the specified city and stores it in the database.

    Parameters
    ----------
    city : str
        The city for which to retrieve the weather data.

    Returns
    -------
    weather_data : dict
        A dictionary containing the current weather data for the specified city.

    """
    # Call the OpenWeatherMap API and retrieve the current weather data
    data = owm_api_call(city)

    # Extract the relevant weather data from the observation object
    weather_data = {
        "City": city,
        "DateTime": datetime.datetime.now(),
        "Temperature": data.weather.temperature("celsius")["temp"],
        "Temperature_max": data.weather.temperature("celsius")["temp_max"],
        "Temperature_min": data.weather.temperature("celsius")["temp_min"],
        "Weather": data.weather.detailed_status,
        "Feels_like": data.weather.temperature("celsius")["feels_like"],
        "Wind_Speed": data.weather.wind()['speed'],
        "Humidity": data.weather.humidity
    }

    # Add the new data to the SQLite3 database
    addWeather(
        weather_data["City"], weather_data["DateTime"], weather_data["Temperature"],
        weather_data["Temperature_max"], weather_data["Temperature_min"],
        weather_data["Weather"], weather_data["Feels_like"],
        weather_data["Wind_Speed"], weather_data["Humidity"]
    )

    return weather_data


# Function to iterate over cities and fetch weather if required
def callCities():
    """
    Iterate over cities and fetch weather data if required.

    The function checks if the last update was more than 5 minutes ago
    and if so, it fetches the weather data for the specified cities.
    The obtained data is added to the SQLite3 database.

    Parameters
    ----------
    None

    Returns
    -------
    data : list
        A list of dictionaries, each containing the current weather data
        for the specified city.

    """
    CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    data = []

    # Check if the last update was more than 5 minutes ago
    if shouldUpdateWeather():
        print("Updating weather data...")
        # Fetch weather data for each city
        for city in CITIES:
            data.append(getWeather(city))
        # Drop data before 24 hours
        dropDataBefore24Hours()
    else:
        print("Skipping, last update was less than 5 minutes ago.")

    return data


# Function to convert Celsius to Fahrenheit
def C2F(C):
    """
    Convert Celsius to Fahrenheit.

    Parameters
    ----------
    C : float
        The temperature in Celsius to convert.

    Returns
    -------
    F : float
        The temperature in Fahrenheit.

    """
    return (C * 9 / 5) + 32


# Function to convert Celsius to Kelvin
def C2K(C):
    """
    Convert Celsius to Kelvin.

    Parameters
    ----------
    C : float
        The temperature in Celsius to convert.

    Returns
    -------
    K : float
        The temperature in Kelvin.

    """
    # The conversion formula is simply adding 273.15 to the Celsius value
    return C + 273.15


# Function to send warning if needed
def warn(city):
    """
    Check if a warning should be triggered for the specified city.

    Parameters
    ----------
    city : str
        The city for which to check if a warning should be triggered.

    Returns
    -------
    str
        The warning message if a warning should be triggered,
        otherwise "No warning".

    """
    if Warning(city):
        # If a warning should be triggered, return the warning message
        return send_warning(city)
    # If no warning should be triggered, return "No warning"
    return "No warning"


# Function to send weather summary
def summary(city):
    """
    Generate and send a weather summary for the specified city.

    Parameters
    ----------
    city : str
        The city for which to generate the weather summary.

    Returns
    -------
    str
        The weather summary message.

    """
    # Retrieve the summary data for the specified city
    data = Summary(city)
    # Save the summary data to the database
    addSummary(city=data["City"], datetime=data["DateTime"], min_temp=data["min_temp"], max_temp=data["max_temp"],
               avg_temp=data["avg_temp"], dominant_weather=data["dominant_weather"])
    # Return the generated weather summary message
    return send_summary(**data)
