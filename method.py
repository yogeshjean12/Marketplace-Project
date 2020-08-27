from app import *
from cart import *
from category import *
from product import *


def get_all_categories():
    categories = db_session.query(Category).all()
    category_list = []
    for category in categories:
        category_list.append(Category(category.id).get_category_details())
    return category_list


def get_all_products(category_id):
    product_list = []
    products = db_session.query(Product).filter_by(category_id=category_id).all()
    for product in products:
        product_list.append(Product(product.id).get_product_details())
    return product_list


def get_cart_products(cart_id):
    cart_product_ids = db_session.query(CartProduct).filter_by(cart_id=cart_id).all()
    cart_product_details = []
    for i in range(len(cart_product_ids)):
        cart_product_details.append(get_cart_product_details(cart_product_ids[i].product_id, cart_id))
    return cart_product_details


def get_cart_product_details(product_id, cart_id):
    cart_products = db_session.query(Product).filter_by(id=product_id).all()
    for row in cart_products:
        product_details = Product(row.id).get_product_details()
        product_details['quantity'] = CartProduct(cart_id, row.id).get_cart_product_quantity()
    return product_details



def get_cart_product_details(product_id, cart_id):
    cart_products = db_session.query(Product).filter_by(id=product_id).all()
    for row in cart_products:
        product_details = Product(row.id).get_product_details()
        product_details['quantity'] = CartProduct(cart_id, row.id).get_cart_product_quantity()
    return product_details


