import requests
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv('../.env.googleAPI')

async def fetch_place_info(address):
  api_key = os.getenv('GOOGLE_API_KEY')
# Base URL
  base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
# Parameters in a dictionary
  params = {
   "input": address,
   "inputtype": "textquery",
   "language": "en",
   "fields": "formatted_address,name,business_status,place_id",
   "key": api_key,
  }
# Send request and capture response
  response = requests.get(base_url, params=params)
# Check if the request was successful
  if response.status_code == 200:
    return response.json()
  else:
    return None



async def fetch_nearby_places(location, radius=1500, keyword=None, type=None):
  api_key = os.getenv('GOOGLE_API_KEY')
# Base URL
  base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
# Parameters in a dictionary
  params = {
    "radius":radius,
    "location":location,
    "key": api_key,
  }

  if keyword:
    params["keyword"] = keyword
  if type:
    params["type"] = type

# Send request and capture response
  response = requests.get(base_url, params=params)
# Check if the request was successful
  if response.status_code == 200:
    return response.json()
  else:
    return None
  

