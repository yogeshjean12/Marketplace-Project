from app import *
from models import *


def get_all_categories():
    categories = db.execute('select * from categories')
    result = [dict(row) for row in categories.fetchall()]
    return result


def get_all_products(category_id):
    products = db.execute('select * from products where category_id = \'{}\''.format(category_id))
    result = [dict(row) for row in products.fetchall()]
    return result


def get_category_name(category_id):
    category_name = db.execute('select name from categories where id = \'{}\''.format(category_id))
    return category_name.fetchone()


def get_seller_name(seller_id):
    seller_name = db.execute('select name from sellers where id = \'{}\''.format(seller_id))
    return seller_name.fetchone()


def get_cart_id(user_id):
    cart_id = db.execute('select id from carts where user_id = \'{}\''.format(user_id))
    return cart_id.fetchone()[0]


def get_product_details(product_id, user_id):
    details = db.execute('select id, name, price, seller_id, category_id '
                         'from products '
                         'where id = \'{}\''.format(product_id))

    for row in details.fetchall():
        result = formate(row,user_id)

    return result


def get_cart_product_quantity(user_id,product_id):
    cart_id = get_cart_id(user_id)

    ordered_quantity = db.execute('select product_quantity '
                                  'from cart_products '
                                  'where cart_id = \'{}\' and product_id = \'{}\''.format(cart_id, product_id))
    result = ordered_quantity.fetchone()[0]
    return result


def formate(row,user_id):
    dic = {}
    dic['product_id'] = row.id
    dic['name'] = row.name
    dic['price'] = row.price
    dic['seller_name'] = get_seller_name(row.seller_id)[0]
    dic['category_name'] = get_category_name(row.category_id)[0]
    dic['ordered_quantity'] = get_cart_product_quantity(user_id, row.id)
    return dic


def get_cart_products(user_id):
    products = db.execute('select product_id '
                          'from cart_products '
                          'where cart_id = (select id from carts where user_id = \'{}\' )'.format(user_id))
    result = [dict(row) for row in products.fetchall()]
    cart_product_details = []
    for i in range(len(result)):
        cart_product_details.append(get_product_details(result[i]['product_id'], user_id))

    return cart_product_details


def remove_product_from_cart(user_id, product_id):
    cart_id = get_cart_id(user_id)
    db.execute('delete from cart_products '
               'where cart_id = \'{}\' and product_id = \'{}\''.format(cart_id, product_id))
    return True


def add_product_to_cart(user_id, product_id):
    cart_id = get_cart_id(user_id)
    id = db.execute('select max(id) from cart_products')
    new_id = (id.fetchone()[0]) + 1
    db.execute('insert into cart_products values(\'{}\',\'{}\',\'{}\',\'1\')'.format(new_id, cart_id, product_id))
    return True


def quantity_check(quantity, product_id, user_id):
    stock = db.execute('select quantity from products where id = \'{}\''.format(product_id))
    ordered_quantity = get_cart_product_quantity(user_id, product_id)
    print(ordered_quantity, quantity)
    if stock.fetchone()[0] > (ordered_quantity+int(quantity)):
        return True
    else:
        return False


def update_product_quantity_in_cart(user_id, quantity, product_id):
    cart_id = get_cart_id(user_id)
    db.execute('update cart_products set product_quantity = \'{}\' '
               'where cart_id =\'{}\' and product_id = \'{}\''.format(quantity, cart_id, product_id))
    return True

