# **TravelSync API**

**Description**  
The **TravelSync API** powers the backend of the TravelSync application, designed to make group itinerary planning effortless. It provides robust functionality for creating and managing itineraries, integrating with services like **Google Places** and **Mapbox** to deliver location-based features. Originally developed during an Agile group project, this API has been independently expanded for enhanced capabilities.

Original group repository:  
[TravelSync API Group Repository](https://github.com/dudleyspence/TravelSync-API-Group)

----------

## **Features**

-   **Group Itinerary Management**: Easily create, edit, and delete group itineraries while inviting friends to collaborate.
-   **Location-Based Services**: Fetch and manage location data using **Google Places API** and visualise it with **Mapbox**.
-   **User Authentication**: Secure login and user management using **Firebase Authentication**.
-   **Dynamic Routing**: Efficiently handle requests with **FastAPI**'s router capabilities.
-   **Data Validation**: Robust data validation using **Pydantic** models for seamless operation.
-   **File Storage**: Upload, download, and delete files securely using **Firebase Storage**.

----------

## **Technologies Used**

-   **Backend Framework**: FastAPI
-   **Database**: MySQL, managed with SQLAlchemy ORM
-   **Validation**: Pydantic for type-safe data validation
-   **APIs**: Google Places API and Firebase Authentication
-   **Hosting**: Deployed via Render  

----------

## **How to Use**

### **Using the API**

1.  The API is designed to serve as the backend for the TravelSync application.
2.  Access endpoints for itinerary management, location data, and file storage through authenticated requests.
3.  For a complete list of endpoints and descriptions, refer to the **API Documentation** (see below).

----------

## **Code Overview**

### **Core Features**

-   **Dynamic Routing**: Modular routing with FastAPI ensures scalability and clarity.
-   **Database Integration**: SQLAlchemy ORM manages efficient data storage and retrieval in MySQL.
-   **Authentication Middleware**: Firebase Authentication secures all user-related operations.

### **Endpoints**

Detailed API documentation is available when running the server:  
Access the Swagger UI at `http://localhost:8000/docs` for a full list of endpoints, parameters, and example requests.

### **Error Handling**

-   Comprehensive error management ensures clear, user-friendly messages for invalid data or unauthorised access.

----------

## **For Developers**

If you wish to contribute or run the project locally, follow these steps:

### **Prerequisites**

-   **Python** (3.8 or higher)
-   **MySQL**

### **Installation**

1.  Clone the repository:  
    `git clone https://github.com/dudleyspence/travelsync-api.git`

2.  Navigate to the project directory:  
    `cd travelsync-api`

3.  Create a virtual environment:  
    `python -m venv venv`  
    Activate it:  
    `source venv/bin/activate` (Windows: `venv\Scripts\activate`)

4.  Install dependencies:  
    `pip install -r requirements.txt`

5.  Configure environment variables:  
    Create a `.env` file with the following:
    ```plaintext
    DATABASE_URL=mysql+pymysql://username:password@localhost/travelsync
    GOOGLE_API_KEY=your_google_places_api_key
    FIREBASE_CONFIG=your_firebase_config
    ```

6.  Set up and seed the database:  
    `python -m src.db.setup_and_seed`

7.  Run the server:  
    `uvicorn src.app:app --reload`

Access the API locally at `http://localhost:8000`.

----------

## **Future Enhancements**

-   **Enhanced Group Management**: Add role-based permissions for itinerary collaborators.
-   **Integration with Calendar APIs**: Allow syncing itineraries with popular calendar services.
-   **Offline Mode**: Implement data caching for limited offline functionality.

----------

## **Contributing**

Contributions are welcome! Fork the repository, make your changes, and submit a pull request for review.

----------

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

----------

## **Related Repositories**



<div align="center">
    <table>
        <tr>
            <td align="center" width="50%">
                <a href="https://github.com/dudleyspence/TravelSync-API-Extended">
                    <img src="https://github-readme-stats.vercel.app/api/pin/?username=dudleyspence&repo=TravelSync-API-Extended&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=0f172a&hide_border=true&locale=en" />
                </a>
            </td>
            <td align="center" width="50%">
                <a href="https://github.com/dudleyspence/TravelSync-FE-Extended">
                    <img src="https://github-readme-stats.vercel.app/api/pin/?username=dudleyspence&repo=TravelSync-FE-Extended&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=0f172a&hide_border=true&locale=en" />
                </a>
            </td>
        </tr>
        <tr>
            <td align="center" width="50%">
                <a href="https://github.com/dudleyspence/TravelSync-FE-Group">
                    <img src="https://github-readme-stats.vercel.app/api/pin/?username=dudleyspence&repo=TravelSync-FE-Group&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=0f172a&hide_border=true&locale=en" />
                </a>
            </td>
            <td align="center" width="50%">
                <a href="https://github.com/dudleyspence/TravelSync-API-Group">
                    <img src="https://github-readme-stats.vercel.app/api/pin/?username=dudleyspence&repo=TravelSync-API-Group&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=0f172a&hide_border=true&locale=en" />
                </a>
            </td>
        </tr>
    </table>
</div>


