This project began as an Agile group for 4 taking part in a project phase. Once this phase ended I decided to independantly continue with the project.

This original group repository can be found here [https://github.com/dudleyspence/TravelSync-API-Group](https://github.com/dudleyspence/TravelSync-API-Group.git)

# TravelSync API

Welcome to the TravelSync API! This RESTful API powers the backend of the TravelSync application, enabling users to create and manage group itineraries with ease. The API integrates with various services, including Google Places and Mapbox, to provide enhanced location-based features.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage and Endpoints](#usage-and-endpoints)
- [Authentication](#authentication)

## Features

- **Group Itinerary Management**: Create, edit, and delete group itineraries and invite friends to collaborate.
- **Location-Based Services**: Fetch location data from Google Places API and visualize it using Mapbox.
- **User Authentication**: Secure user login and management using Firebase Authentication.
- **Dynamic Routing**: Efficient routing with FastAPI's router capabilities.
- **Data Validation**: Robust data validation using Pydantic models.
- **File Storage**: Upload, download and delete files using firebase filestorage.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **MySQL**: Relational database management system for efficient data storage and retrieval.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Google Places API**: To fetch and manage location data.
- **Firebase Authentication**: For secure user authentication.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/travelsync-api.git
   cd travelsync-api
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root directory and add the following variables:

   ```plaintext
   DATABASE_URL=mysql+pymysql://username:password@localhost/travelsync
   GOOGLE_API_KEY=your_google_places_api_key
   FIREBASE_CONFIG=your_firebase_config
   ```

5. **Run database setup and seed**:

   ```bash
   python -m src.db.setup_and_seed
   ```

6. **Start the FastAPI server**:

   ```bash
   fastapi dev src/app.py
   ```

## Usage and Endpoints

Once the server is running, you can access the API documentation at `http://localhost:8000/docs` (Swagger UI)

Refer to the [API Documentation](http://localhost:8000/docs) for a complete list of endpoints and their descriptions.

## Authentication

Authentication is handled using Firebase Authentication. Users must be authenticated to perform actions such as creating or modifying itineraries. Include the Firebase Auth token in the request headers as follows:
