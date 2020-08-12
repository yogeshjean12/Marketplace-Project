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
def home_page():

    categories = get_all_categories()
    return jsonify(categories)


@app.route('/categories/<category_id>/products', methods=['GET'])
def category_page(category_id):

    products = get_all_products(category_id)
    return jsonify(products)


@app.route('/cart/user/<user_id>/', methods=['GET'])
def view_cart(user_id):

    result = get_cart_products(user_id)
    return jsonify(result)

