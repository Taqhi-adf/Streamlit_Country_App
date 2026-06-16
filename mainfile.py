import os
import requests
from dotenv import load_dotenv

# Load your environment variables (optional but recommended for keys)
load_dotenv()

# Replace with your actual key from restcountries.com, or use os.getenv("REST_COUNTRIES_KEY")
API_KEY = "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"

# Setting up headers required for v5 authentication
headers = {"Authorization": f"Bearer {API_KEY}"}

# 1. Fetching all countries (Updated to v5 domain and authentication)
response_all = requests.get(
    "https://api.restcountries.com/v5/countries", headers=headers
)
print("All Countries Status:", response_all.status_code)

# 2. Fetching India specifically using the updated v5 search patterns
# Note: You can also use parameters or full-text query depending on v5 documentation
response_india = requests.get(
    "https://api.restcountries.com/v5/countries?q=india", headers=headers
)

if response_india.status_code == 200:
    data = response_india.json()
    print("\nIndia Data Parsed Successfully!")
    # Prints the data payload
    print(data)
else:
    print(f"Error {response_india.status_code}: {response_india.text}")