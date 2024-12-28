"""
Code that is 100% ChatGPT. 
"""
import requests

# Your session cookie value (keep this secret!)
SESSION_COOKIE = ""

# Define the year and day for the input you want to fetch
YEAR = 2024
MIN_DAY = 21
MAX_DAY = 26
for DAY in range(MIN_DAY,MAX_DAY):

    # URL for the input
    INPUT_URL = f"https://adventofcode.com/{YEAR}/day/{DAY}/input"

    # Headers with your session cookie
    HEADERS = {
        "Cookie": f"session={SESSION_COOKIE}",
        "User-Agent": "YourUserAgentHere (your-email@example.com)"
    }

    # Fetch the input
    response = requests.get(INPUT_URL, headers=HEADERS)

    # Check if the request was successful
    if response.status_code == 200:
        print("Input fetched successfully!")
        input_data = response.text
        with open(f"inputs/input{DAY}",'w') as file:  # Or save to a file
            file.write(input_data)
    else:
        print(f"Failed to fetch input: {response.status_code}")