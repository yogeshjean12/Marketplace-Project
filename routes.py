from app import *
from models import *


@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = User(user_name, password)
        if user.is_valid() == True:
            session['user_id'] = user.get_user_id()
            session['login status'] = True
            return 'Login'
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

    cart_id = Cart(user_id).get_cart_id()
    result = get_cart_products(cart_id)
    return jsonify(result)


@app.route('/cart/<user_id>', methods=['DELETE'])
def delete_product_from_cart(user_id):

    product_id = request.form['product_id']
    cart_id = Cart(user_id).get_cart_id()
    CartProduct(cart_id, product_id).remove_product_from_cart()
    return 'Product deleted from cart successfully'


@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):

    product_id = request.form['product_id']
    cart_id = Cart(user_id).get_cart_id()
    CartProduct(cart_id, product_id).add_product_to_cart()
    return 'Product added to cart successfully'


@app.route('/cart/<user_id>', methods=['PUT'])
def update_quantity(user_id):
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    cart_id = Cart(user_id).get_cart_id()
    if Product(product_id).quantity_check(quantity) == True:
        CartProduct(cart_id, product_id).update_product_quantity_in_cart(quantity)
        return 'Product quantity in cart get updated'
    else:
        return 'Out of stock'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('login_status', None)
    return 'Logged out'

