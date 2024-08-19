from fastapi.testclient import TestClient
from tests.test_functions.test_utils import is_non_empty_string, is_valid_coordinates

from src.app import app


client = TestClient(app)


def test_places_info():
    input_address = {"address": "LS29 8EL"}
    response = client.post("/api/places/info", json=input_address)  # json= ensures the body is JSON
    assert response.status_code == 200

    place_info = response.json().get("placeInfo", [])

    for place in place_info:
        assert is_non_empty_string(place["formatted_address"])
        assert is_non_empty_string(place["name"])
        assert is_non_empty_string(place["place_id"])
        assert is_valid_coordinates(place["geometry"]["location"])

