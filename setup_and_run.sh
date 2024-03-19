#!/bin/bash

# Step 1: Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
echo "Virtual environment created."

# Step 2: Activate the virtual environment and install packages
echo "Activating virtual environment and installing packages..."
source venv/bin/activate
pip install -r requirements.txt
echo "Packages installed."

# Step 3: Run main.py using uvicorn
echo "Starting the FastAPI app with Uvicorn..."
uvicorn main:app --reload &
# Ensuring backend services start properly
sleep 10

# Step 4: Change directory to frontend and install npm packages
echo "Changing directory to frontend and installing NPM packages..."
cd frontend || exit
npm install
echo "NPM packages installed."

# Step 5: Run the frontend development server
echo "Starting frontend development server..."
npm run dev

# Notify user the script has finished running
echo "Setup and servers are up and running."