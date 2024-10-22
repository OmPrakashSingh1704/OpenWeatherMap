import concurrent.futures

import streamlit as st

from DataManager.DataGen import callCities
from DataManager.Users_db import initialize_db as u_db
from DataManager.report_db import initialize_db as r_db
from DataManager.weather_db import initialize_db as w_db
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Run the initialization functions in parallel
def initialize_dbs_async():
    """Run the initialization functions in parallel using a ThreadPoolExecutor.

    This function runs the initialization functions for the weather database,
    report database, and users database in parallel. Additionally, it calls
    the callCities function that fetches the weather data for all cities.

    :return: None
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run the initialization functions in parallel
        future_w_db = executor.submit(w_db)
        future_r_db = executor.submit(r_db)
        future_u_db = executor.submit(u_db)
        # Fetch the weather data for all cities
        future_callCities = executor.submit(callCities)
        # You can use the futures if you need the results or status, for now, it's just fire-and-forget


# Call the async initialization
initialize_dbs_async()

# Set up the page
st.set_page_config(page_title="WEATHER_MONITOR", layout="wide")

# Home page content
st.title("Welcome to the Weather Monitoring App")

# Introduction
st.write("""
Welcome to **Weather Monitor**, your go-to solution for tracking weather, managing users, and generating weather reports.
Explore the functionalities below or navigate using the sidebar.
""")

# Create columns for detailed explanations
col1, col2, col3 = st.columns(3)

# User Management
with col1:
    st.markdown("### [**User Management**](Users)")
    st.write("""
    - Create and manage user profiles.
    - Track user activity and interactions.
    - Assign roles and manage access controls.
    """)

# Weather Monitoring
with col2:
    st.markdown("### [**Weather Monitoring**](Weather)")
    st.write("""
    - Get real-time weather updates for any location.
    - Receive alerts for severe weather conditions.
    - Compare current data with historical trends.
    """)

# Weather Reports
with col3:
    st.markdown("### [**Weather Reports**](Report)")
    st.write("""
    - Generate detailed weather reports with summaries.
    - Analyze dominant weather conditions.
    - Export reports for offline access.
    """)

# Final note
st.write("---")
st.write("""
Use the sidebar to navigate to any section. Whether monitoring weather conditions, managing users, or generating reports, **Weather Monitor** has you covered.
""")
