# EV Management Web Application

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Session Management](#session-management)
- [Error Handling](#error-handling)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

This project is a web application built using Flask that allows users to manage and compare Electric Vehicle (EV) data. Users can add new EV models, edit and delete EV details, view a list of all EVs, search for EVs based on multiple criteria, and compare EV specifications. Google Cloud Datastore is used for data storage, and Firebase authentication is used for user login.

## Features

- **EV Management**: Users can add, edit, and delete EV models along with their specifications.
- **Search EVs**: Search for EVs based on parameters like name, manufacturer, year, battery size, range, cost, and power.
- **Compare EVs**: Select and compare multiple EVs based on their specifications.
- **User Authentication**: User authentication via Google Firebase to ensure secure access to the application.
- **Review and Rating System**: Users can leave reviews and ratings for EV models, and view average scores.
- **Google Cloud Datastore Integration**: EV data is stored in Datastore, with review and rating data managed separately.

## Requirements

- Python 3.x
- Flask
- Google Cloud SDK
- Google Cloud Datastore
- Google Firebase

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ev-management-flask-app.git
   cd ev-management-flask-app
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Google Cloud**

   - Ensure that you have Google Cloud SDK installed and authenticated.
   - Create a Google Cloud project and enable Datastore and Firebase.
   - Set up your project configuration.

6. **Run the Flask Application**

   ```bash
   python app.py
   ```

## Usage

1. **Sign In**: Users authenticate using Google Firebase. A user session is created, and the user's email and name are stored in the Datastore.
2. **Add EVs**: Users can add EV models with their name, manufacturer, year, battery size, WLTP range, cost, and power.
3. **Search EVs**: Users can search for EV models by filtering based on name, manufacturer, year range, battery size range, range, cost, and power.
4. **Compare EVs**: Compare multiple EV models based on their specifications.
5. **Rate and Review**: Users can provide ratings and reviews for EVs, and view an average rating for each model.

## API Endpoints

- **`GET /`**: Displays the list of EV models. Handles user authentication via Google Firebase.
- **`POST /add_evs`**: Loads the form to add a new EV.
- **`POST /add_ev`**: Adds a new EV model to the datastore.
- **`POST /search`**: Searches EVs based on multiple filters.
- **`POST /show_ev`**: Displays details for a specific EV.
- **`POST /edit`**: Loads the form to edit an EV's details.
- **`POST /edit_ev`**: Updates an EV's details.
- **`POST /delete`**: Deletes an EV from the datastore.
- **`POST /compare_evs_page`**: Loads the page to compare multiple EVs.
- **`POST /compare_evs`**: Displays a comparison of the selected EVs.
- **`POST /add_rating`**: Adds a review and rating for a specific EV.

## Session Management

Session data is managed using Flask's session object and cookies. Each session stores:
- `name`: The name of the authenticated user.
- `email`: The email address of the authenticated user.

Google Firebase handles authentication, and the session ensures secure access to EV data.

## Error Handling

- **Authentication Errors**: If the user's Firebase token is invalid, the application displays an error message.
- **Duplicate EV**: If an EV with the same name, manufacturer, and year already exists, the application prevents adding duplicates.
- **Search and Filter Errors**: Ensures that the input values for filtering are valid and filters the EVs accordingly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Google Cloud](https://cloud.google.com/) for Datastore and Firebase.
- [Werkzeug](https://werkzeug.palletsprojects.com/) for utilities related to security and routing.
