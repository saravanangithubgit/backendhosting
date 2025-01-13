import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

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
    # Set the port using the environment variable, defaulting to 5000 if not provided
    port = int(os.getenv("PORT", 5000))
    # Run the Flask app on all IPs and the dynamic port
    app.run(host="0.0.0.0", port=port)

