import concurrent.futures
import datetime

import streamlit as st

from DataManager.DataGen import callCities
from DataManager.LLMsummary import send_summary, send_warning
from DataManager.Users_db import get_users_by_city as Users
from DataManager.Users_db import subscribe, unsubscribe
from DataManager.mailSystem import send_email
from DataManager.weather_db import Summary, Warning


# Run callCities in parallel
def run_callCities_async():
    """
    Run the callCities function in parallel using a ThreadPoolExecutor.

    Returns:
        concurrent.futures.Future: The future object returned by the executor.
    """
    # Create a ThreadPoolExecutor to run the callCities function in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the callCities function to the executor and get the future object
        future = executor.submit(callCities)
        # Return the future object
        return future


# Start callCities asynchronously
future_callCities = run_callCities_async()

st.set_page_config(layout="wide")


@st.dialog("Subscribe")
def Subscribe() -> None:
    """
    Opens a dialog to subscribe a user to receive weather updates.

    The user is asked to enter their username, email address, and city.
    Once the user confirms, the subscription details are added to the database.
    """
    # Get the user's name
    UserName: str = st.text_input("Username")
    # Get the user's email address
    Mail: str = st.text_input("Mail")
    # Get the user's city
    City: str = st.radio(
        "What City do you live in?",
        ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    )
    # If the user confirms, add the subscription to the database
    if st.button("confirm"):
        subscribe(UserName, Mail, City)
        st.success("Subscription successful!")
        st.rerun()


@st.dialog("Unsubscribe")
def Unsubscribe() -> None:
    """
    Opens a dialog to unsubscribe a user from receiving weather updates.

    The user is asked to enter their email address.
    Once the user confirms, the subscription is removed from the database.
    """
    # Get the user's email address
    Mail: str = st.text_input("Enter Mail")
    # If the user confirms, unsubscribe the user
    if st.button("confirm"):
        unsubscribe(Mail)
        st.success("Unsubscription successful!")
        st.rerun()


# Apply custom CSS for styling
st.markdown("""
    <style>
        .container {
            background-color: #f9f9f9;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
        }
        .title {
            color: #4CAF50;
            font-weight: bold;
            font-size: 40px;
            text-align: center;
        }
        .description {
            color: #331;
            font-size: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and page description
st.markdown('<div class="title"> User Management</div>', unsafe_allow_html=True)
st.write("### Manage your subscription preferences to receive weather reports and warnings.")

# Create two columns
col1, col2 = st.columns(2)

# Subscribe container
with col1:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    with st.container(border=True, height=250):
        st.subheader("Subscribe/Change city preference")
        st.markdown("""
            <p class="description">
            Stay updated with the latest weather reports and warnings. 
            By subscribing, you'll receive regular updates about weather conditions in your region.
            </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        _, x, _ = st.columns(3)
        with x:
            if st.button("Subscribe"):
                Subscribe()

# Unsubscribe container
with col2:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    with st.container(border=True, height=250):
        st.subheader("Unsubscribe")
        st.markdown("""
            <p class="description">
            Don't want to receive reports anymore? You can easily unsubscribe here.
            You'll stop receiving weather notifications and updates.
            </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        _, x, _ = st.columns(3)
        with x:
            if st.button("Unsubscribe"):
                Unsubscribe()

# Weather notifications logic
if datetime.datetime.now().hour == 22:
    for city in ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]:
        data = Summary(city)
        for user, mail in Users(city):
            send_email("Weather Report", send_summary(User=user, **data), mail)

# Warning notifications logic
for city in ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]:
    if Warning(city):
        for user, mail in Users(city):
            send_email("Weather Warning", send_warning(User=user, city=city), mail)
