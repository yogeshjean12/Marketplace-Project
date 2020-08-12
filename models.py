from sqlalchemy.orm import relationship

from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class User(base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(20), nullable=False)
    password = Column(String(60), nullable=False)

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


class Category(base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)


class Seller(base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    def get_seller_name(self):
        seller_name = db.execute('select name from sellers where id = \'{}\''.format(self.id))
        return seller_name


class Product(base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    product_quantity = Column(Integer, nullable=False)


class Cart(base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))


class CartProduct(base):
    __tablename__ = 'cart_products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
