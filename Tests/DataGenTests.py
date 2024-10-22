import unittest

from DataManager.DataGen import *
from DataManager.report_db import initialize_db as r_db
from DataManager.weather_db import initialize_db as w_db

# Initialize the databases before running the tests
w_db()
r_db()


class MyTestCase(unittest.TestCase):

    def test_owm_api(self):
        """Test the OWM API call for a specific city.

        This test case calls the owm_api_call function with the city name "Delhi"
        and checks if the returned value is not None.
        """
        # Call the OWM API for the city "Delhi"
        call = owm_api_call("Delhi")

        # Check if the returned value is not None
        self.assertIsNotNone(call)

    def test_getWeather(self):
        """Test fetching weather data for a specific city.

        This test case calls the getWeather function with the city name "Delhi"
        and checks if the returned value is not None.
        """
        # Call the getWeather function for the city "Delhi"
        data = getWeather("Delhi")

        # Check if the returned value is not None
        self.assertIsNotNone(data)

    def test_callCities(self):
        """Test the callCities function to ensure it returns a list of cities.

        This test case calls the callCities function and checks if the returned
        value is a list of cities. It does not check the contents of the list.
        """
        data = callCities()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_C2F(self):
        """Test Celsius to Fahrenheit conversion.

        This test case calls the C2F function with the value 32 and checks if
        the returned value is 89.6.
        """
        self.assertAlmostEqual(C2F(32), 89.6, places=1)

    def test_C2K(self):
        """Test Celsius to Kelvin conversion.

        This test case calls the C2K function with the value 32 and checks if
        the returned value is 305.15.
        """
        self.assertAlmostEqual(C2K(32), 305.15, places=2)

    def test_warn(self):
        """Test the warning function for high temperatures.

        This test case calls the warn function with the city name "Delhi" and
        checks if the returned value matches the expected output.
        """
        # Check if a warning should be triggered
        if Warning("Delhi"):
            # If a warning should be triggered, check if the returned value
            # matches the expected output
            self.assertEqual(warn("Delhi"), send_warning("Delhi"))
        else:
            # If a warning should not be triggered, check if the returned value
            # matches the expected output
            self.assertEqual(warn("Delhi"), "No warning")

    def test_summary(self):
        """Test fetching the summary for a specific city.

        This test case calls the summary function with the city name "Delhi"
        and checks if the returned value is not None.
        """
        self.assertIsNotNone(summary("Delhi"))


if __name__ == '__main__':
    unittest.main()
