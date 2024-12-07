# Anime Recommendation System

This project implements a REST API-based Anime Recommendation System using the AniList GraphQL API as the data source. The system allows users to search for anime, get recommendations, and manage preferences while providing secure JWT-based authentication.

---

## Features

- **Anime Search**: Search anime by name or genre.
- **Recommendations**: Get personalized anime recommendations based on user preferences.
- **User Management**: Register, login, and manage user preferences.
- **Authentication**: JWT-based secure authentication.
- **Database**: PostgreSQL integration for storing user data and preferences.
- **API Documentation**: Automatically generated API docs with `drf-yasg`.

---

## Prerequisites

Ensure the following software is installed:

- Python 3.9+
- PostgreSQL 12+
- Git
- Virtual Environment Tool (e.g., `venv` or `virtualenv`)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/GaganDureja/anime-recommendation-system.git
cd anime-recommendation-system
```
### 2. Set Up Environment Variables
```bash
python -m venv env
```
### 3. Install Dependencies
#### On Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL
- Download pgadmin or Log into PostgreSQL
- Create a user with name **postgres**, password **123** (you can change this to your own but remember to update the same in settings.py)
- Create a database name anime_recommendation and select postgres user to access all

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Start the Development Server
#### On Linux/MacOS:
```bash
python3 manage.py runserver
```
#### On Windows:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- **POST** `/auth/register`: Register a new user.
- **POST** `/auth/login`: Login and retrieve a JWT token.

### Anime
- **GET** `/anime/search`: Search anime by name or genre.
- **GET** `/anime/recommendations`: Get recommendations (requires authentication).

### User Preferences
- **POST** `/user/preferences`: Add/Update user preferences.
