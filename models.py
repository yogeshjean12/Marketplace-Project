from app import *
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, user_name, password):
        self._user_name = user_name
        self._password = password

    def is_valid(self):
        _user = db_session.query(User).filter_by(user_name=self._user_name).first()
        if _user.user_name == self._user_name and _user.password == self._password:
            return True
        else:
            return False

    def get_user_id(self):
        _user = db_session.query(User).filter_by(user_name=self._user_name).first()
        return _user.user_id


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, category_id):
        self._category_id = category_id

    def get_category_name(self):
        _category = db_session.query(Category).filter_by(id=self._category_id).first()
        return _category.name

    def get_category_details(self):
        _category = db_session.query(Category).filter_by(id=self._category_id).first()
        category_dict = {}
        category_dict['category_id'] = _category.id
        category_dict['category_name'] = _category.name
        return category_dict


class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, seller_id):
        self._seller_id = seller_id

    def get_seller_name(self):
        _seller = db_session.query(Seller).filter_by(id=self._seller_id).first()
        return _seller.name


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    quantity = Column(Integer, nullable=False)

    def __init__(self, product_id):
        self._product_id = product_id

    def get_product_details(self):
        _product = db_session.query(Product).filter_by(id=self._product_id).first()
        product_dict = {}
        product_dict['product_id'] = _product.id
        product_dict['product_name'] = _product.name
        product_dict['price'] = _product.price
        product_dict['category_name'] = Category(_product.category_id).get_category_name()
        product_dict['seller_name'] = Seller(_product.seller_id).get_seller_name()
        product_dict['quantity'] = _product.quantity
        return product_dict

    def quantity_check(self, quantity):
        _product = db_session.query(Product).filter_by(id=self._product_id).first()
        if _product.quantity >= (int(quantity)):
            return True
        else:
            return False


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    def __init__(self, _user_id):
        self._user_id = _user_id

    def get_cart_id(self):
        _cart = db_session.query(Cart).filter_by(user_id=self._user_id).first()
        return _cart.id


class CartProduct(Base):
    __tablename__ = 'cart_products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product_quantity = Column(Integer, nullable=False)

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
        _cart_product = db_session.query(CartProduct).filter_by(cart_id=self._cart_id,
                                                                product_id=self._product_id).first()
        db_session.delete(_cart_product)
        db_session.commit()
        return True

    def update_product_quantity_in_cart(self, quantity):
        _cart_product = db_session.query(CartProduct).filter_by(cart_id=self._cart_id,
                                                                product_id=self._product_id).first()
        _cart_product.product_quantity = quantity
        db_session.add(_cart_product)
        db_session.commit()
        return True

    def get_cart_product_quantity(self):
        _cart_product = db_session.query(CartProduct).filter_by(cart_id=self._cart_id,
                                                                product_id=self._product_id).first()
        return _cart_product.product_quantity


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

