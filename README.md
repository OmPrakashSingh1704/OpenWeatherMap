# Weather Reporting Application

This application provides weather reports for various cities using the OpenWeather API. It calculates daily summaries and sends email notifications with the weather information(LLM Backed).

## Features

- [x] Fetches weather data for multiple cities.
- [x] Calculates daily maximum, minimum, and average temperatures.
- [x] Determines the dominant weather condition for each day.
- [x] Sends email notifications with weather summaries.
- [x] Provides mail-based updates and warnings based on severe weather conditions.
- [x] Generates detailed reports using a language model (LLM) for enhanced understanding of the weather data.
- [x] Visualizes weather trends and statistics for better insights.
- [ ] Weather forecasts (requires subscription of OpenWeatherMap API)

## Requirements

To run the application, you'll need to have Python installed along with the necessary packages listed in `requirements.txt`.

## Environment Variables

Before running the application, you need to configure the following environment variables:

1. Create a `.env` file in the root directory of the project and add the following lines, replacing the placeholders with your actual credentials:

   ```plaintext
   OPENWEATHER_API_KEY=<your-openweather-api-key>
   SENDER_MAIL=<your-email-address>
   SENDER_PASSWORD=<your-email-password>
   ```

   - **`OPENWEATHER_API_KEY`**: Your API key from [OpenWeather](https://home.openweathermap.org/api_keys).
   - **`SENDER_MAIL`**: The email address you want to use to send weather reports.
   - **`SENDER_PASSWORD`**: The [password](https://myaccount.google.com/apppasswords) for the sender email account.

     **Note: Your original password will not work due to new Google policies make sure you generate one from [here](https://myaccount.google.com/apppasswords).**

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/OmPrakashSingh1704/OpenWeatherMap/
   cd OpenWeatherMap
   ```

2. **Create and activate venv:**
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```
3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Setup Script:**

   Execute the provided `bash.sh` script to run the application:

   ```bash
   .\bash.sh
   ```

3. **Run the Application:**

   After setting up the environment variables, the application will run automatically when you execute the bash script.

## Usage

- The application will fetch the weather data, process it, and send email notifications at 10:00 pm or wheneven temerature raises above 35°C. It will also provide updates and warnings via email for severe weather conditions, generate comprehensive reports using LLMs, and visualize weather trends.
