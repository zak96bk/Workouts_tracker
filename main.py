import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
GENDER = "male"
WEIGHT_KG = 83
HEIGHT_CM = 180
AGE = 27

# API URLs and headers
url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
sheety_url = os.getenv('SHEETY')
headers = {
    'x-app-id': os.getenv('APP_ID'),
    'x-app-key': os.getenv('API_KEY')
}

# User input
user_query = input("Enter your exercise : ")

# Parameters for Nutritionix API
parameters = {
    "query": user_query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Request data from Nutritionix API
response = requests.post(url, headers=headers, json=parameters)

# Check if request was successful
if response.status_code == 200:
    exercise_data = response.json()
    exercises = exercise_data.get("exercises", [])

    # Log exercises to Sheety
    current_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    sheety_headers = {"Authorization": f"Bearer {os.getenv('TOKEN')}"}

    for exercise in exercises:
        sheety_body = {
            "workout": {
                "date": current_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": int(exercise["duration_min"]),
                "calories": exercise["nf_calories"]
            }
        }

        # Send data to Sheety API
        response_sheety = requests.post(sheety_url, json=sheety_body, headers=sheety_headers)
        if response_sheety.status_code == 200:
            print("Exercise logged successfully:", response_sheety.json())
        else:
            print("Failed to log exercise to Sheety:", response_sheety.text)
else:
    print("Failed to fetch exercise data from Nutritionix:", response.text)
