# database.py
import json
import os

# File path for the JSON file
DB_FILE = 'data.json'

# Function to initialize the database (if it doesn't exist)
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, mode='w') as file:
            json.dump([], file)  # Initialize an empty list

# Function to store form data in the JSON file
def store_data(name, email, message):
    # Load existing data from the JSON file
    with open(DB_FILE, mode='r') as file:
        data = json.load(file)
    
    # Add new form data to the list
    data.append({
        'name': name,
        'email': email,
        'message': message
    })

    # Write updated data back to the JSON file
    with open(DB_FILE, mode='w') as file:
        json.dump(data, file, indent=4)