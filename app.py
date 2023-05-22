# BEGIN CODE HERE
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get('name')

    products = mongo.db.products.find({"name": {"$regex": name, "$options": "i"}}) # Query the MongoDB database for products matching the name

    products.sort("price", -1) # Sort the products by price in descending order

    search_results = [] # Prepare the list of search results
    for product in products:
        search_results.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "production_year": product["production_year"],
            "price": product["price"],
            "color": product["color"],
            "size": product["size"]
        })

    return jsonify(search_results) # Return the search results as a JSON response

    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    product_data = request.get_json()

    required_fields = ['id', 'name', 'production_year', 'price', 'color', 'size'] # Validate the required fields in the product_data
    for field in required_fields:
        if field not in product_data:
            return jsonify({'message': f'Missing required field: {field}'}), 400


    existing_product = mongo.db.products.find_one({'name': product_data['name']})     # Check if a product with the same name already exists in the database

    if existing_product: # Update the existing product with the new data
        existing_product['price'] = product_data['price']
        existing_product['production_year'] = product_data['production_year']
        existing_product['color'] = product_data['color']
        existing_product['size'] = product_data['size']
        mongo.db.products.update_one({'_id': existing_product['_id']}, {'$set': existing_product})
        return jsonify({'message': 'Product updated successfully'})
    else:  # Insert the new product into the database
        mongo.db.products.insert_one(product_data)
        return jsonify({'message': 'Product added successfully'})

    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE

    def calculate_similarity(query_vector, item_vectors):  # Helper function to calculate cosine similarity
        similarities = cosine_similarity(query_vector.reshape(1, -1), item_vectors)
        return similarities[0]

    query_data = request.get_json()

    required_fields = ['id', 'name', 'production_year', 'price', 'color', 'size']  # Validate the required fields in the query_data
    for field in required_fields:
        if field not in query_data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    product_vectors = []  # Get all product vectors from the database
    product_names = []
    for product in mongo.db.products.find():
        product_vectors.append([product['production_year'], product['price'], product['color'], product['size']])
        product_names.append(product['name'])

    query_vector = np.array([query_data['production_year'], query_data['price'], query_data['color'], query_data['size']]) # Calculate the similarity scores
    similarities = calculate_similarity(query_vector, np.array(product_vectors))

    threshold = 0.7 # Filter products based on similarity threshold

    similar_products = [name for name, similarity in zip(product_names, similarities) if similarity > threshold]

    return jsonify({'similar_products': similar_products})

    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    semester = request.args.get('semester', type=int)

    url = f'https://qa.auth.gr/el/x/studyguide/600000438/{semester}' # Construct the URL based on the provided semester

    options = webdriver.ChromeOptions() # Configure the Selenium WebDriver
    options.add_argument('--headless')  # Run the browser in headless mode (without GUI)
    driver = webdriver.Chrome(options=options)  # Replace with the path to your ChromeDriver

    driver.get(url)  # Navigate to the URL

    course_elements = driver.find_elements_by_css_selector('.course .course-title') # Find the elements containing the course names

    course_names = [element.text for element in course_elements] # Extract the course names

    driver.quit() # Close the browser

    return jsonify({'course_names': course_names})
    # END CODE HERE

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
