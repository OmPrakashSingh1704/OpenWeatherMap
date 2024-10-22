# Weather Summary App

## Overview

The Weather Summary App provides daily weather data summaries for multiple cities. It fetches real-time weather information, calculates temperature statistics, and stores summaries in a SQLite database. This application is built using Python and Streamlit for a user-friendly interface.

## Features

- Fetches weather data for multiple cities (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad).
- Calculates daily maximum, minimum, and average temperatures.
- Determines the dominant weather condition for each day.
- Stores and retrieves summaries in a SQLite database.
- Interactive visualization of weather data using Plotly.

## Installation and Running the App

To simplify the setup process, a bash script is provided. This script will create a virtual environment, install the required dependencies, and run the application.

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/weather-summary-app.git
   cd weather-summary-app
   ```

2. Run the bash script:

   ```bash
   .\bash.sh
   ```

   This script will:
   - Create a virtual environment.
   - Install the necessary packages from `requirements.txt`.
   - Start the Streamlit app.

3. Once the setup is complete, open your browser and navigate to `http://localhost:8501` to access the Weather Summary App.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
