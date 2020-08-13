from app import db


class User:

    def __init__(self, user_name, password):
        self._user_name = user_name
        self._password = password

    def is_username_valid(self):

        _user_name = db.execute('select user_name '
                               'from users '
                               'where user_name = \'{}\' '.format(self._user_name))

        if _user_name.fetchone() is None:
            return False
        else:
            return True

    def is_password_valid(self):
        _user_password = db.execute('select * '
                                   'from users '
                                   'where password =  \'{}\''.format(self._password))

        if _user_password.fetchone() is None:
            return False
        else:
            return True

    def get_user_id(self):
        _user_id = db.execute('select user_id '
                             'from users '
                             'where user_name = \'{}\' '.format(self._user_name))
        result = _user_id.fetchone()[0]
        return result


class Category:

    def __init__(self, category_id):
        self._category_id = category_id

    def get_category_name(self):
        category_name = db.execute('select name from categories where id = \'{}\''.format(self._category_id))
        return category_name.fetchone()[0]


class Seller:

    def __init__(self, seller_id):
        self._seller_id = seller_id

    def get_seller_name(self):
        seller_name = db.execute('select name from sellers where id = \'{}\''.format(self._seller_id))
        return seller_name.fetchone()[0]


class Product:

    def __init__(self, product_id):
        self._product_id = product_id

    def quantity_check(self, quantity):
        stock = db.execute('select quantity from products where id = \'{}\''.format(self._product_id))
        if stock.fetchone()[0] >= (int(quantity)):
            return True
        else:
            return False


class Cart:

    def __init__(self, user_id):
        self._user_id = user_id

    def get_cart_id(self):
        cart_id = db.execute('select id from carts where user_id = \'{}\''.format(self._user_id))
        return cart_id.fetchone()[0]


class CartProduct:

    def __init__(self, cart_id, product_id):
        self._cart_id = cart_id
        self._product_id = product_id

    def add_product_to_cart(self):
        db.execute('insert into cart_products '
                   'values(\'{}\',\'{}\',\'{}\',\'1\')'.format(self.__get_new_id(), self._cart_id, self._product_id))
        return True

    def __get_new_id(self):
        id = db.execute('select max(id) from cart_products')
        new_id = (id.fetchone()[0]) + 1
        return new_id

    def remove_product_from_cart(self):
        db.execute('delete from cart_products '
                   'where cart_id = \'{}\' and product_id = \'{}\''.format(self._cart_id, self._product_id))
        return True

    def update_product_quantity_in_cart(self, quantity):
        db.execute('update cart_products set product_quantity = \'{}\' '
                   'where cart_id =\'{}\' and product_id = \'{}\''.format(quantity, self._cart_id, self._product_id))
        return True

    def get_cart_product_quantity(self):
        ordered_quantity = db.execute('select product_quantity '
                                      'from cart_products '
                                      'where cart_id = \'{}\' and product_id = \'{}\''.format(self._cart_id, self._product_id))
        result = ordered_quantity.fetchone()[0]
        return result


def get_all_categories():
    categories = db.execute('select * from categories')
    result = [dict(row) for row in categories.fetchall()]
    return result


def get_all_products(category_id):
    products = db.execute('select * from products where category_id = \'{}\''.format(category_id))
    result = [dict(row) for row in products.fetchall()]
    return result


def get_cart_products(cart_id):
    products = db.execute('select product_id '
                          'from cart_products '
                          'where cart_id = \'{}\' '.format(cart_id))
    result = [dict(row) for row in products.fetchall()]
    cart_product_details = []
    for i in range(len(result)):
        cart_product_details.append(get_cart_product_details(result[i]['product_id'], cart_id))

    return cart_product_details


def get_cart_product_details(product_id, cart_id):
    details = db.execute('select id, name, price, seller_id, category_id '
                         'from products '
                         'where id = \'{}\''.format(product_id))

    for row in details.fetchall():
        result = __formate(row, cart_id)

    return result


def __formate(row, cart_id):
    dic = {}
    dic['product_id'] = row.id
    dic['name'] = row.name
    dic['price'] = row.price
    dic['seller_name'] = Seller(row.seller_id).get_seller_name()
    dic['category_name'] = Category(row.category_id).get_category_name()
    dic['ordered_quantity'] = CartProduct(cart_id, row.id).get_cart_product_quantity()
    return dic


