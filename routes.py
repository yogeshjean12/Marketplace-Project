from flask_cors import cross_origin

from app import *
from method import *
from user import *
from product import *
from cart import *




@cross_origin()
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_name = data['username']
    password = data['password']
    confirm_password = data['confirm_password']
    user = User(user_name, password)
    if user.register_user(confirm_password) == True:
        return jsonify({'status': '200'})
    else:
        return jsonify({'status': '401'})

@cross_origin()
@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        data = request.get_json()
        user_name = data['username']
        password = data['password']
        user = User(user_name, password)
        if user.is_valid() == True:
            session['user_id'] = user.get_user_id()
            user_id = session['user_id']
            print(user_id)
            return jsonify({'status': '200', 'user_id': user.get_user_id()})
        else:
            return jsonify({'status': '401'})

@cross_origin()
@app.route('/categories', methods=['GET'])
def display_categories():

        categories = get_all_categories()
        return jsonify(categories)

@cross_origin()
@app.route('/categories/<category_id>/products', methods=['GET'])
def display_products(category_id):

    products = get_all_products(category_id)
    return jsonify(products)

@cross_origin()
@app.route('/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    cart_id = Cart(user_id).get_cart_id()
    result = get_cart_products(cart_id)
    return jsonify(result)

@cross_origin()
@app.route('/cart/<user_id>', methods=['DELETE'])
def delete_product_from_cart(user_id):
    data = request.get_json()
    product_id = data['product_id']
    cart_id = Cart(user_id).get_cart_id()
    CartProduct(cart_id, product_id).remove_product_from_cart()
    return jsonify({'status': '200'})

@cross_origin()
@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    product_id = data['product_id']
    cart_id = Cart(user_id).get_cart_id()
    if CartProduct(cart_id, product_id).add_product_to_cart() == True:

        return jsonify({'status': '200'})
    else:
        return jsonify({'status': '401'})


@cross_origin()
@app.route('/cart/<user_id>', methods=['PUT'])
def update_quantity(user_id):
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    cart_id = Cart(user_id).get_cart_id()
    if Product(product_id).quantity_check(quantity) == True:

        CartProduct(cart_id, product_id).update_product_quantity_in_cart(quantity)
        return jsonify({'status': '200'})
    else:
        return jsonify({'status': '401'})

