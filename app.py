# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient, ASCENDING, DESCENDING
from werkzeug.utils import secure_filename
from tasks import process_csv_file
from models import get_movies_paginated
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# JWT Setup
jwt = JWTManager(app)

# MongoDB Setup
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.imdb
uploads_collection = db.uploads

# Helper function for user authentication
def authenticate_user(username, password):
    # Hardcoded for simplicity; replace with your auth logic
    return username == "admin" and password == "password"

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if authenticate_user(username, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/api/upload-csv', methods=['POST'])
@jwt_required()
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join("/tmp", filename)
    file.save(filepath)

    # Initiate background task
    task = process_csv_file.apply_async(args=[filepath])
    upload_id = str(task.id)

    # Store initial upload record in DB
    uploads_collection.insert_one({
        "_id": upload_id,
        "status": "processing",
        "progress": 0
    })

    return jsonify({"upload_id": upload_id}), 202

@app.route('/api/upload-progress/<upload_id>', methods=['GET'])
@jwt_required()
def upload_progress(upload_id):
    upload = uploads_collection.find_one({"_id": upload_id})
    if not upload:
        return jsonify({"error": "Upload not found"}), 404

    return jsonify({
        "status": upload['status'],
        "progress": upload['progress']
    }), 200

@app.route('/api/movies', methods=['GET'])
@jwt_required()
def get_movies():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    sort_by = request.args.get("sort_by", "date_added")
    order = DESCENDING if request.args.get("order", "desc") == "desc" else ASCENDING

    movies, total_movies = get_movies_paginated(page, page_size, sort_by, order)
    return jsonify({
        "total": total_movies,
        "movies": movies
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
