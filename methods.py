from app import db


def get_all_categories():
    categories = db.execute('select * from online_shopping.categories')
    return categories.fetchall()


def get_all_products():
    products = db.execute('select * from online_shopping.products where category_id = \'2\'')
    return products.fetchall()
