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