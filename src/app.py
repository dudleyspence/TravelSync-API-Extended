from fastapi import FastAPI
from src.controllers.google_places_controllers import router as google_places_router
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.users_controllers import router as users_router
from src.controllers.groups_controllers import router as groups_router
from src.controllers.events_controllers import router as events_router
from src.controllers.group_members_controllers import router as group_members_router
from src.controllers.itineraries_controllers import router as itineraries_router

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(users_router, prefix="/api")

app.include_router(google_places_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the TravelSync API"}


# address = "2 Bath Street LS29 8EL"

# location = "-33.8670522, 151.1957362"
# radius=20