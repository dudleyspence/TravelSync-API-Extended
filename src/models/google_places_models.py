import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os


# Load the environment variables from the .env file
load_dotenv("../TravelSync-API/.env.googleAPI") 
# needed in development but not on render 

async def fetch_place_info(address):
  api_key = os.getenv('GOOGLE_API_KEY')
  
  # Print the API key to verify it's loaded correctly
  if api_key:
    print("API Key loaded successfully:", api_key)
  else:
    print("hello")
    print("API Key not found. Please check your .env file and path.")

# Base URL
  base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
# Parameters in a dictionary
  params = {
   "input": address,
   "inputtype": "textquery",
   "language": "en",
   "fields": "formatted_address,name,business_status,place_id,geometry",
   "key": api_key,
  }

  async with httpx.AsyncClient() as client:
    response = await client.get(base_url, params=params)
    if response.status_code == 200:
            # we are dealing with a JSON object and python intead uses a dictionary for this
            # if we just used ["candidates"] this could throw a keyError if there wasnt candidates
            # dictionaries have the .get(key, default_value)
            # having a default value avoids the keyError 
            locationInfo = response.json().get("candidates", [])
            # the request might be successful 200 but return no results so we need to force a 404 not found
            if not locationInfo:
              print(locationInfo)
              raise HTTPException(status_code=404, detail="No results found")
            
            return locationInfo

    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching place info")


async def fetch_nearby_places(location, radius, place_type):
  api_key = os.getenv('GOOGLE_API_KEY')

  # Print the API key to verify it's loaded correctly
  if api_key:
      print("API Key loaded successfully:", api_key)
  else:
      print("API Key not found. Please check your .env file and path.")
      
# Base URL
  base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
# Parameters in a dictionary
  params = {
    "radius":radius,
    "location":location,
    "type": place_type,
    "key": api_key,
  }

  async with httpx.AsyncClient() as client:
    response = await client.get(base_url, params=params)
  if response.status_code == 200:
    nearbyPlaces = response.json().get("results", [])

      # the request might be successful 200 but return no results so we need to force a 404 not found
    if not nearbyPlaces:
      raise HTTPException(status_code=404, detail="No results found")
     
    filtered_nearbyPlaces = []

    # Iterate over all places and filter each one
    for place in nearbyPlaces:
        filtered_place = {
            "name": place.get("name", ""),
            "co-ords": place.get("geometry", {}).get("location", {}),
            "place_id": place.get("place_id", ""),
            "rating": place.get("rating", None),
            "user_ratings_total": place.get("user_ratings_total", None),
            "types": place.get("types", [])
        }
        filtered_nearbyPlaces.append(filtered_place)

    return filtered_nearbyPlaces
  
  else:
      raise HTTPException(status_code=response.status_code, detail="Error fetching nearby places")



  
