import sqlite3

import pandas as pd


# Initialize the SQLite database and create the 'reports' table if it doesn't exist
def initialize_db():
    """
    Initialize the SQLite database and create the 'reports' table if it doesn't exist.

    This function creates a table named 'reports' in the 'report.db' database if it doesn't already exist.
    The table has the following columns:
        City: The name of the city.
        DateTime: The date and time of the report.
        min_temp: The minimum temperature in the report.
        max_temp: The maximum temperature in the report.
        avg_temp: The average temperature in the report.
        dominant_weather: The dominant weather condition in the report.
    The City and DateTime columns are set as the primary key to ensure that there is only one report per city per day.
    """
    conn = sqlite3.connect('report.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    City TEXT,
                    DateTime TEXT,
                    min_temp REAL,
                    max_temp REAL,
                    avg_temp REAL,
                    dominant_weather TEXT,
                    PRIMARY KEY (City, DateTime)  -- Ensure uniqueness on these columns
                );
                ''')
    conn.commit()
    conn.close()


# Add or update a weather summary report for a given city
def addSummary(city, datetime, min_temp, max_temp, avg_temp, dominant_weather):
    """
    Add or update a weather summary report for a given city.

    This function adds or updates a weather summary report for the given city.
    If the city and datetime pair already exists, the existing record is updated.
    Otherwise, a new record is inserted into the 'reports' table.

    Parameters
    ----------
    city : str
        The name of the city.
    datetime : str
        The date and time of the report in the format '%Y-%m-%d %H:%M:%S.%f'.
    min_temp : float
        The minimum temperature in the report.
    max_temp : float
        The maximum temperature in the report.
    avg_temp : float
        The average temperature in the report.
    dominant_weather : str
        The dominant weather condition in the report.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('report.db')
    c = conn.cursor()

    # Insert or replace the new data into the reports table
    c.execute('''INSERT OR REPLACE INTO reports 
                 (City, DateTime, min_temp, max_temp, avg_temp, dominant_weather)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (city, datetime, min_temp, max_temp, avg_temp, dominant_weather))

    conn.commit()
    conn.close()


# Retrieve all weather summary reports and return them as a DataFrame
def getSummary():
    """
    Retrieve all weather summary reports and return them as a DataFrame.

    This function executes a query to fetch all data from the 'reports' table
    and returns the result as a DataFrame.

    Returns
    -------
    df : pandas.DataFrame
        A DataFrame containing all weather summary reports.
    """
    conn = sqlite3.connect('report.db')
    c = conn.cursor()

    # Execute a query to fetch all data from the 'reports' table
    c.execute("SELECT * FROM reports")
    data = c.fetchall()

    # Get column names
    col_names = [description[0] for description in c.description]
    conn.close()

    # Create a DataFrame using the fetched data and column names
    df = pd.DataFrame(data, columns=col_names)
    return df
