from pymongo import MongoClient, ASCENDING, DESCENDING
from config import Config

mongo = MongoClient(Config.MONGO_URI)
db = mongo.imdb
movies_collection = db.movies
uploads_collection = db.uploads

def insert_movie(movies):
    movies_collection.insert_many(movies)

def update_upload_status(upload_id, status, progress):
    uploads_collection.update_one(
        {"_id": upload_id},
        {"$set": {"status": status, "progress": progress}}
    )

def get_movies_paginated(page, page_size, sort_by, order):
    total_movies = movies_collection.count_documents({})
    movies = list(
        movies_collection.find()
        .sort(sort_by, order)
        .skip((page - 1) * page_size)
        .limit(page_size)
    )
    return movies, total_movies
