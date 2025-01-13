import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from urllib.parse import quote  # Replacing the deprecated werkzeug import

app = Flask(__name__)
CORS(app)

# MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://saravanantechexpert:1232003@cluster.rhxap.mongodb.net/?retryWrites=true&w=majority")

# Ensure the URI is loaded correctly
if not mongo_uri:
    raise ValueError("MongoDB URI is not set in environment variables")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["ecommerdb"]
products_collection = db["product"]

@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")  # Get category from query parameter
    query = {"category": category} if category else {}
    products = list(products_collection.find(query, {"_id": 0}))  # Exclude _id field from results
    return jsonify(products)

@app.route("/product/<string:product_id>", methods=["GET"])
def get_product(product_id):
    product = products_collection.find_one({"id": product_id}, {"_id": 0})  # Search by product id
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    # Change the port to match environment variable or default to 5000
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT environment variable is not set
    app.run(host="0.0.0.0", port=port, debug=True)  # Listen on all IP addresses (host="0.0.0.0")
