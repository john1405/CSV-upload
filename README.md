
# IMDB CSV Upload System

## Overview
This project allows users to upload large CSV files containing movie or show data to a MongoDB database. Users can track the upload progress and view data through a paginated API. The project uses Flask for the web server, MongoDB for storage, and Celery with Redis for background processing.

## Features
- User authentication with JWT
- Upload large CSV files (up to 10GB)
- Track upload progress
- Paginated API to view and sort movie/show data

## Tech Stack
- **Backend**: Flask
- **Database**: MongoDB (using PyMongo)
- **Task Queue**: Celery
- **Broker**: Redis
- **Data Processing**: Pandas

---

## Prerequisites
- Python 3.8+
- MongoDB (installed and running)
- Redis (for Celery task queue)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/imdb-csv-upload-system.git
cd imdb-csv-upload-system

### 2. install dependency
  - pip install -r requirements.txt

### 3. setup redis

### 4. setup environment variable

### 5. Run celery worker

### 6. Run the flask application