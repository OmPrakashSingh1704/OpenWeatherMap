from concurrent.futures import ThreadPoolExecutor

import plotly.express as px
import streamlit as st

from DataManager.DataGen import callCities, C2K, C2F
from DataManager.LLMsummary import send_summary
from DataManager.report_db import getSummary
from DataManager.weather_db import Summary, allSummary

st.set_page_config(layout="wide")

st.markdown("# Summary/Report 📃")

CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]


def convert_temperature(temp: float, unit: str) -> float:
    """
    Convert temperature from Celsius to the specified unit.

    Args:
    temp (float): The temperature in Celsius.
    unit (str): The unit to convert to. Options are "Celsius", "Kelvin", or "Fahrenheit".

    Returns:
    float: The converted temperature.
    """
    if unit == "Celsius":
        # No conversion needed, just round to 2 decimal places
        return round(temp, 2)
    elif unit == "Kelvin":
        # Convert to Kelvin
        return round(C2K(temp), 2)
    elif unit == "Fahrenheit":
        # Convert to Fahrenheit
        return round(C2F(temp), 2)


def display_current_summary(city):
    """Display the current weather summary for the specified city.

    If the summary data is a dictionary, it will be passed to the send_summary
    function to generate a natural language summary. If not, an error message
    will be displayed.

    Args:
        city (str): The city for which to display the summary.
    """
    summary_data = Summary(city)
    if isinstance(summary_data, dict):  # Ensure summary_data is a dictionary
        # Pass the summary data to the send_summary function to generate a
        # natural language summary. The City key is passed separately to ensure
        # it is not included in the **kwargs.
        current_summary = send_summary(City=summary_data['City'],
                                       **{k: v for k, v in summary_data.items() if k != 'City'})
        st.subheader("Current Weather Summary")
        st.write(current_summary)
    else:
        # If the summary data is not a dictionary, display an error message
        st.error(f"Failed to retrieve summary for {city}: {summary_data}")


def plot_weather_summary(todaysummarydata, city):
    """Plot the weather summary data for the specified city.

    Args:
        todaysummarydata (dict): The summary data for the specified city.
        city (str): The city for which to display the summary data.

    Returns:
        None
    """
    if todaysummarydata:
        fig = px.line_polar(
            r=[todaysummarydata["min_temp"], todaysummarydata["avg_temp"],
               todaysummarydata["max_temp"]],
            theta=["Min Temp", "Avg Temp", "Max Temp"],
            line_close=True,
            title=f"Today's Summary for {city}",
            template="plotly_dark"
        )
        # Set the area of the polar plot to be filled
        fig.update_traces(fill='toself')
        st.plotly_chart(fig, key=f"{city}_todaysummary")
    else:
        # Display an error message if the summary data is not available
        st.warning(f"No summary data available for {city}.")


def display_city_data(city):
    """Display weather data for the specified city.

    This function displays the weather data for the specified city. It first
    displays the current summary, then allows the user to select the temperature
    unit. It then retrieves the summary data for the city and converts the
    temperatures based on the selected unit. It then plots a polar chart of the
    weather summary data for the specified city.

    Args:
        city (str): The city for which to display the weather data.

    Returns:
        None
    """
    # Display current summary
    display_current_summary(city)

    # Select temperature unit
    unit = st.radio("Unit", ["Celsius", "Fahrenheit", "Kelvin"], key=f"{city}_unit", horizontal=True)
    """Select the unit for the weather data. The unit options are:
    - Celsius
    - Fahrenheit
    - Kelvin
    """

    # Retrieve summary data for the city
    summary_data = Summary(city)
    weather_summary_till_today = getSummary()
    weather_summary_till_today = weather_summary_till_today[weather_summary_till_today['City'] == city]
    """Retrieve the summary data for the specified city. The summary data
    includes the minimum, maximum and average temperatures for the city.
    """

    if all(key in summary_data for key in ["min_temp", "max_temp", "avg_temp"]):
        # Convert temperatures based on the selected unit
        min_temp = convert_temperature(summary_data["min_temp"], unit)
        max_temp = convert_temperature(summary_data["max_temp"], unit)
        avg_temp = convert_temperature(summary_data["avg_temp"], unit)
        """Convert the temperatures based on the selected unit. The conversion
        is done using the convert_temperature function.
        """

        weather_summary_till_today['min_temp'] = weather_summary_till_today['min_temp'].apply(
            lambda x: convert_temperature(x, unit))
        weather_summary_till_today['max_temp'] = weather_summary_till_today['max_temp'].apply(
            lambda x: convert_temperature(x, unit))
        weather_summary_till_today['avg_temp'] = weather_summary_till_today['avg_temp'].apply(
            lambda x: convert_temperature(x, unit))
        """Convert the temperatures in the summary data for the city based on
        the selected unit.
        """

        # Prepare a summary dictionary for visualization
        todaysummarydata = {
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp
        }

        # Plot today's weather summary
        plot_weather_summary(todaysummarydata, city)

    else:
        st.error("Temperature data is incomplete.")
    with st.expander(f"Weather Data till today for {city}"):
        st.dataframe(weather_summary_till_today.style.background_gradient(cmap='Blues'), use_container_width=True,
                     hide_index=True)


# Create tabs for each city
tabs = st.tabs(CITIES)

# Fetch all summaries in parallel
with ThreadPoolExecutor() as executor:
    executor.submit(callCities())
    # Retrieve all daily summaries concurrently and save them
    executor.submit(allSummary)  # Call to save daily summaries in the database

# Display data for each city within its respective tab
for i, city in enumerate(CITIES):
    with tabs[i]:
        display_city_data(city)
