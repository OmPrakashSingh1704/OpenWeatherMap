import threading
import time

import pandas as pd
import plotly.express as px
import streamlit as st

from DataManager.DataGen import C2K, C2F, callCities
from DataManager.LLMsummary import send_summary, send_warning
from DataManager.weather_db import Summary, Warning
from DataManager.weather_db import getWeather

st.set_page_config(layout="wide")
st.markdown("# Weather Monitoring App 🌦️")


@st.cache_data(ttl=60)  # Cache the data for 60 seconds
def get_data_from_database() -> pd.DataFrame:
    """
    Retrieve the weather data from the SQLite database and return it as a Pandas DataFrame.
    The data is cached for 60 seconds to reduce the number of queries to the database.

    Returns:
        pd.DataFrame: The weather data.
    """
    return getWeather()


# Function to display weather data for a city
def display_city_data(city, df):
    """
    Display the weather data and summary for the specified city.

    Parameters
    ----------
    city : str
        The city for which to display the weather data.
    df : pd.DataFrame
        The weather data DataFrame.
    """
    current_summary = send_summary(**Summary(city))
    st.subheader("Current Weather Summary")
    st.write(current_summary)
    col1, col2 = st.columns(2)

    # Select temperature unit
    with col1:
        Unit = st.radio("Select Unit:", ["°C", "°K", "°F"], key=f"{city}_unit", horizontal=True)

    # Display warnings or success message
    with col2:
        if Warning(city):
            st.warning(send_warning("VISITOR", city))
        else:
            st.success("Weather looks good!")

    df_city = df[df["City"] == city]

    # Apply temperature conversions based on the selected unit
    if Unit == "°C":
        df_city["Temperature"] = df_city["Temperature"].apply(lambda x: round(x, 2))
    elif Unit == "°K":
        df_city["Temperature"] = df_city["Temperature"].apply(lambda x: round(C2K(x), 2))
    elif Unit == "°F":
        df_city["Temperature"] = df_city["Temperature"].apply(lambda x: round(C2F(x), 2))

    # Display a line chart for weather data
    fig = px.line(df_city, x="DateTime", y=["Temperature", "Temperature_max", "Temperature_min", "feels_like"],
                  title=f"Weather Data for {city}")
    st.plotly_chart(fig)

    # Display humidity and wind speed
    fig = px.line(df_city, x="DateTime", y=["Humidity", "Wind_Speed"], title=f"Humidity Data for {city}")
    st.plotly_chart(fig)

    # Display weather summary
    with st.expander(f"Weather Data for {city}"):
        st.dataframe(df_city.style.background_gradient(cmap='Blues'), use_container_width=True, hide_index=True)


def fetch_weather_data():
    """
    Fetches weather data from the database every 30 seconds and reruns the app to refresh the displayed data.

    This function runs in an infinite loop, so it should be run in a separate thread.
    """
    while True:
        df = get_data_from_database()  # Fetch data from DB
        time.sleep(30)  # Refresh every 30 seconds
        st.experimental_rerun()  # Rerun the app to refresh the displayed data


# Start data fetching in a separate thread
threading.Thread(target=fetch_weather_data, daemon=True).start()

callCities()  # Dump data into the DB

# List of cities
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Create tabs for each city
tabs = st.tabs(CITIES)

# Display data for each city within its respective tab
df = get_data_from_database()
for i, city in enumerate(CITIES):
    with tabs[i]:
        display_city_data(city, df)
