# fitness-tracker
# Fitness Tracker API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

A RESTful API for tracking fitness activities built with Django and Django REST Framework.

## Features

- **User Authentication**: JWT token-based authentication
- **Activity Tracking**: Log workouts with type, duration, distance, and calories
- **CRUD Operations**: Create, read, update, and delete activities
- **Metrics Dashboard**: View workout statistics and trends
- **Filtering/Sorting**: Filter by date range or activity type

## Tech Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: JWT Tokens
- **API Documentation**: Swagger/Redoc

## Setup Instructions

### Prerequisites
- Python 3.10+
- Pipenv (recommended) or pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HASSAN-AMIMOU/fitness-tracker.git
   cd fitness-tracker