from app import *
from models import *
from methods import *


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = User(user_name, password)

        if user.is_username_valid():
            if user.is_password_valid():
                return 'Login successful'
            else:
                return 'Invalid username or password'
        else:
            return 'Invalid username or password'


@app.route('/categories', methods=['GET'])
def display_categories():
    categories = get_all_categories()
    return jsonify(categories)


@app.route('/categories/<category_id>/products', methods=['GET'])
def display_products(category_id):
    products = get_all_products(category_id)
    return jsonify(products)


@app.route('/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    result = get_cart_products(user_id)
    return jsonify(result)


@app.route('/cart/<user_id>/delete_product', methods=['DELETE'])
def delete_product_from_cart(user_id):
    product_id = request.form['product_id']
    remove_product_from_cart(user_id, product_id)
    return 'Product deleted from cart successfully'


@app.route('/cart/<user_id>/add_product', methods=['POST'])
def add_to_cart(user_id):
    product_id = request.form['product_id']
    add_product_to_cart(user_id, product_id)
    return 'Product added to cart successfully'


@app.route('/cart/<user_id>/update_quantity', methods=['PUT'])
def update_quantity(user_id):

    product_id = request.form['product_id']
    quantity = request.form['quantity']
    if quantity_check(quantity, product_id, user_id) == True:
        update_product_quantity_in_cart(user_id, quantity, product_id)
        return 'Product quantity in cart get updated'
    else:
        return 'Out of stock'

