#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found! Please ensure it exists in the current directory."
    exit 1
fi

# Create a virtual environment (optional)
if [ ! -d venv ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
venv\Scripts\activate

# Install required packages
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

# Run the application
echo "Running the application..."
streamlit run 🏠_Home.py # Replace 'app.py' with your application's entry point if different

# Deactivate the virtual environment (optional)
deactivate
