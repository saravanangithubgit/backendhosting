from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  


client = MongoClient("mongodb+srv://saravanantechexpert:1232003@cluster.rhxap.mongodb.net/?retryWrites=true&w=majority")
db = client["ecommerdb"]  
products_collection = db["product"]  


@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")  
    query = {"category": category} if category else {}
    products = list(products_collection.find(query, {"_id": 0}))  
    return jsonify(products)


@app.route("/product/<string:product_id>", methods=["GET"])
def get_product(product_id):
    product = products_collection.find_one({"id": product_id}, {"_id": 0})
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
