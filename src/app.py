from fastapi import FastAPI
from src.controllers.google_places_controllers import router as google_places_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)




app.include_router(google_places_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the TravelSync API"}


# address = "2 Bath Street LS29 8EL"

# location = "-33.8670522, 151.1957362"
# radius=20