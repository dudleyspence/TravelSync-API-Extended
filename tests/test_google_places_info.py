# tests/test_places.py
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from controllers.google_places_controllers import router as google_places_router


app = FastAPI()
app.include_router(google_places_router)

client = TestClient(app)