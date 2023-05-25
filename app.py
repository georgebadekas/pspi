# BEGIN CODE HERE
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import numpy as np

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])




@app.route("/search", methods=["GET"])
def search(): 
    # BEGIN CODE HERE
    name = request.args.get("name")
    query = {"name": {"$regex": name}}
    results = mongo.db.products.find(query)
    results.sort("price", -1)
    
    search_results = [] 
    for product in results:
        search_results.append({
            "id": str(product["id"]),
            "name": product["name"],
            "production_year": product["production_year"],
            "price": product["price"],
            "color": product["color"],
            "size": product["size"]
        })
    
    return jsonify(search_results) 

    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    
    json_document = request.get_json()
    products_validator = {
        "id": str,
        "name": str,
        "production_year": int,
        "price": int,
        "color": int,
        "size": int
    }
    for key in products_validator:
        if key not in json_document:
            
            response = 'JSON is invalid: Missing key '+ str(key)
            return jsonify({'message': f'{response}'}), 400
        result = isinstance(json_document[key],products_validator[key])
        if not(result):
            response = 'JSON is invalid: ' + str(key) + ' has to be a' + str(products_validator[key])
            return jsonify({'message': f'{response}'}), 400
        if key == "color" and (json_document[key] > 3 or json_document[key]<1):
            response = "JSON is invalid: field color has to be between 1 and 3" 
            return jsonify({'message': f'{response}'}), 400
        if key == "size" and (json_document[key] > 4 or json_document[key] < 1):
            response = "JSON is invalid: field size has to be between 1 and 4"
            return jsonify({'message': f'{response}'}), 400

    product_data = request.get_json()
 
    existing_product = mongo.db.products.find_one({'name': product_data['name']}) 
    if existing_product: 
        existing_product['price'] = product_data['price']
        existing_product['production_year'] = product_data['production_year']
        existing_product['color'] = product_data['color']
        existing_product['size'] = product_data['size']
        mongo.db.products.update_one({'_id': existing_product['_id']}, {'$set': existing_product})
        return jsonify({'message': 'Product updated successfully'})
    else:  
        mongo.db.products.insert_one(product_data)
        return jsonify({'message': 'Product added successfully'})
  
   
   
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    #validating the json we recieved
    json_document = request.get_json()
    products_validator = {
        "id": str,
        "name": str,
        "production_year": int,
        "price": int,
        "color": int,
        "size": int
    }
    for key in products_validator:
        if key not in json_document:
            
            response = 'JSON is invalid: Missing key '+ str(key)
            return jsonify({'message': f'{response}'}), 400
        result = isinstance(json_document[key],products_validator[key])
        if not(result):
            response = 'JSON is invalid: ' + str(key) + ' has to be a' + str(products_validator[key])
            return jsonify({'message': f'{response}'}), 400
        if key == "color" and (json_document[key] > 3 or json_document[key]<1):
            response = "JSON is invalid: field color has to be between 1 and 3" 
            return jsonify({'message': f'{response}'}), 400
        if key == "size" and (json_document[key] > 4 or json_document[key] < 1):
            response = "JSON is invalid: field size has to be between 1 and 4"
            return jsonify({'message': f'{response}'}), 400
    product_vectors = []  
    product_names = []
    for product in mongo.db.products.find():
        product_vectors.append([product['production_year'], product['price'], product['color'], product['size']])
        product_names.append(product['name'])     
    
    json_vector = [json_document['production_year'], json_document['price'],json_document['color'],json_document['size']]
    
    results = []

    #here we will calculate the similarity for each product
    i = 0
    for product in product_vectors:
       
        if (np.dot(product, json_vector) / (np.linalg.norm(product) * np.linalg.norm(json_vector))) * 100 >= 70:
            results.append(product_names[i])
        i = i + 1


    return jsonify({'similar_products': results})
    
    
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    
    semester = request.args.get('semester', type=int)
    if semester > 8 or semester < 0 :
        return "BAD REQUEST", 400
    id_of_table = "exam" + str(semester)
    url = f"https://qa.auth.gr/el/x/studyguide/600000438/current" # Construct the URL based on the provided semester
    results = []
    try:
        options = Options()
        # does not apper as window
        options.headless = True
        # setting a chrome browser
        driver = webdriver.Chrome(options=options)
        # goes to the specified url
        driver.get(url)

        table = driver.find_element(By.ID, id_of_table)
        rows_of_table = table.find_elements(By.TAG_NAME,"tr")
        i = 1
        for row in rows_of_table:
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                if i % 4 == 2:
                    results.append(cell.text)
                i = i + 1
        driv
        return results, 200
    except Exception as e:
        return "BAD REQUEST", 400

    # END CODE HERE

