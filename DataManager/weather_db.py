import datetime
import sqlite3

import pandas as pd

from DataManager.report_db import addSummary


# Initialize the SQLite database and create the 'weather' table if it doesn't exist
def initialize_db():
    """
    Initialize the SQLite database and create the 'weather' table if it doesn't exist.

    The 'weather' table contains the following columns:
    City: The city for which the weather data is recorded.
    DateTime: The date and time when the weather data was recorded.
    Temperature: The current temperature in degree Celsius.
    Temperature_max: The maximum temperature in degree Celsius for the day.
    Temperature_min: The minimum temperature in degree Celsius for the day.
    Weather: The current weather condition.
    feels_like: The feels like temperature in degree Celsius.
    Wind_Speed: The wind speed in km/h.
    Humidity: The humidity percentage.
    """
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather (
                 City TEXT, 
                 DateTime TEXT, 
                 Temperature REAL, 
                 Temperature_max REAL, 
                 Temperature_min REAL, 
                 Weather TEXT, 
                 feels_like REAL,
                 Wind_Speed REAL, 
                 Humidity REAL)''')
    conn.commit()
    conn.close()


# Add a new weather record to the 'weather' table
def addWeather(City, DateTime, Temperature, Temperature_max, Temperature_min, Weather, feels_like, Wind_Speed,
               Humidity):
    """
    Add a new weather record to the 'weather' table.

    Parameters
    ----------
    City : str
        The city for which the weather data is recorded.
    DateTime : str
        The date and time when the weather data was recorded.
    Temperature : float
        The current temperature in degree Celsius.
    Temperature_max : float
        The maximum temperature in degree Celsius for the day.
    Temperature_min : float
        The minimum temperature in degree Celsius for the day.
    Weather : str
        The current weather condition.
    feels_like : float
        The feels like temperature in degree Celsius.
    Wind_Speed : float
        The wind speed in km/h.
    Humidity : float
        The humidity percentage.
    """
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()
    c.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (
                  City, DateTime, Temperature, Temperature_max, Temperature_min, Weather, feels_like, Wind_Speed,
                  Humidity))
    conn.commit()
    conn.close()


# Retrieve all weather data from the 'weather' table and return it as a DataFrame
def getWeather():
    """
    Retrieve all weather data from the 'weather' table and return it as a DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the weather data.
    """
    # Connect to the database
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()

    # Fetch all data from the 'weather' table
    c.execute("SELECT * FROM weather")
    data = c.fetchall()

    # Get column names from the database
    col_names = [description[0] for description in c.description]

    # Close the database connection
    conn.close()

    # Create a DataFrame using the fetched data and column names
    df = pd.DataFrame(data, columns=col_names)

    # Print the DataFrame for debugging purposes
    print(df)

    # Return the DataFrame
    return df


# Check if the weather data should be updated (if more than 6 minutes have passed)
def shouldUpdateWeather():
    """
    Checks if the weather data should be updated.

    It does this by checking the time difference between the current time
    and the time of the last entry in the 'weather' table. If more than 6
    minutes (360 seconds) have passed, it returns True, indicating that
    the weather data should be updated.

    Returns
    -------
    bool
        True if the weather data should be updated, False otherwise.
    """
    # Connect to the database
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()

    # Retrieve the last entry from the 'weather' table
    c.execute("SELECT DateTime FROM weather ORDER BY DateTime DESC LIMIT 1")
    last_entry = c.fetchone()

    # Close the database connection
    conn.close()

    # If no entry exists, update the weather
    if not last_entry:
        return True

    # Calculate the time difference since the last entry
    last_datetime = datetime.datetime.strptime(last_entry[0], '%Y-%m-%d %H:%M:%S.%f')
    time_difference = datetime.datetime.now() - last_datetime

    # Return True if more than 6 minutes (360 seconds) have passed
    return time_difference.total_seconds() >= 360


# Delete weather data older than 24 hours
def dropDataBefore24Hours():
    """
    Deletes weather data older than 24 hours from the database.

    This function is called periodically to ensure that the database does not
    grow indefinitely.
    """
    # Connect to the database
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()

    # Delete all weather data older than 24 hours
    c.execute("DELETE FROM weather WHERE DateTime < datetime('now', '-24 hours')")

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()


# Check if a warning should be triggered (if the last two temperatures are above 35°C)
def Warning(city):
    """
    Check if a warning should be triggered for the specified city.

    This function checks the last two temperature entries for the specified
    city and returns True if both temperatures are above 35°C, indicating a
    warning should be triggered.

    Parameters
    ----------
    city : str
        The city for which to check the temperatures.

    Returns
    -------
    bool
        True if a warning should be triggered, False otherwise.
    """
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()
    c.execute("SELECT Temperature FROM weather WHERE City = ? ORDER BY DateTime DESC LIMIT 2", (city,))
    last_two_temps = c.fetchall()
    conn.close()

    # If there are less than 2 temperature entries, do not trigger a warning
    if len(last_two_temps) < 2:
        return False

    # Trigger a warning if both of the last two temperatures are above 35°C
    return last_two_temps[0][0] > 35 and last_two_temps[1][0] > 35


def allSummary():
    """
    Fetches summary statistics for each city for every day.

    This function fetches the maximum, minimum, and average temperatures for each
    city for every day since the data has been collected. It also fetches the
    most frequent weather status for each day for each city. The resulting data
    is stored in the 'reports' database table.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()

    # Fetch summary statistics for each city for every day
    c.execute("""
        SELECT 
            City, 
            Date(DateTime) AS Date, 
            MAX(Temperature) AS max_temp, 
            MIN(Temperature) AS min_temp, 
            AVG(Temperature) AS avg_temp
        FROM weather
        GROUP BY City, Date(DateTime)
    """)
    daily_summaries = c.fetchall()

    for summary in daily_summaries:
        city = summary[0]
        date = summary[1]
        max_temp = summary[2]
        min_temp = summary[3]
        avg_temp = summary[4]

        # Fetch the most frequent weather status for each day for this city
        c.execute("""
            SELECT Weather
            FROM weather
            WHERE City = ? AND Date(DateTime) = ?
            GROUP BY Weather
            ORDER BY COUNT(*) DESC
            LIMIT 1
        """, (city, date))
        mode_status = c.fetchone()

        # Set the most frequent weather status, or default to 'Unknown'
        dominant_weather = mode_status[0] if mode_status else "Unknown"

        # Save the summary for this city using addSummary
        addSummary(
            city,
            date,
            max_temp,
            min_temp,
            avg_temp,
            dominant_weather
        )

    conn.close()


# Generate a daily weather summary for a given city
def Summary(city):
    """
    Generate a daily weather summary for the given city.

    :param city: The city for which to generate the summary.
    :return: A dictionary with the following keys:
        City: The city for which the summary was generated.
        DateTime: The date of the summary.
        max_temp: The maximum temperature recorded for that day.
        min_temp: The minimum temperature recorded for that day.
        avg_temp: The average temperature recorded for that day.
        dominant_weather: The most frequent weather status for that day.
    """
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()

    # Fetch the summary statistics for the current day
    c.execute("""
        SELECT City, Date(DateTime), MAX(Temperature), MIN(Temperature), AVG(Temperature)
        FROM weather
        WHERE City = ? AND Date(DateTime) = Date('now')
        GROUP BY Date(DateTime)
    """, (city,))
    daily_summaries = c.fetchone()

    # Fetch the most frequent weather status for the current day
    c.execute("""
        SELECT Weather
        FROM weather
        WHERE City = ? AND Date(DateTime) = Date('now')
        GROUP BY Weather
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """, (city,))
    mode_status = c.fetchone()
    conn.close()

    # Set the most frequent weather status, or default to 'Unknown'
    dominant_weather = mode_status[0] if mode_status else "Unknown"

    # Return a dictionary with the daily summary
    return {
        "City": daily_summaries[0],
        "DateTime": daily_summaries[1],
        "max_temp": daily_summaries[2],
        "min_temp": daily_summaries[3],
        "avg_temp": daily_summaries[4],
        "dominant_weather": dominant_weather
    }
