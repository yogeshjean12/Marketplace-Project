from app import db
from sqlalchemy import Column, Integer, String


class User:
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(20), nullable=False)
    password = Column(String(60), nullable=False)

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def is_username_valid(self):
        user_name = db.execute('select user_name '
                               'from online_shopping.users '
                               'where user_name = \'{}\' '.format(self.user_name))

        if user_name.fetchone() is None:
            return False
        else:
            return True

    def is_password_valid(self):
        user_password = db.execute('select * '
                                   'from online_shopping.users '
                                   'where password =  \'{}\''.format(self.password))

        if user_password.fetchone() is None:
            return False
        else:
            return True

    def get_user_id(self):
        user_id = db.execute('select user_id '
                             'from online_shopping.users '
                             'where user_name = \'{}\''.format(self.user_name))
        return user_id.fetchone()


class Category:
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(20), nullable=False)
    category_description = Column(String(100), nullable=True)


class Seller:
    __tablename__ = 'sellers'
    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_name = Column(String(20), nullable=False)


class Product:
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(20), nullable=False)
    category_id = Column(Integer, foreign_key=True)
    seller_id = Column(Integer, foreign_key=True)
    product_quantity = Column(Integer, nullable=False)



class Cart:
    __tablename__ = 'carts'
    user_id = Column(Integer, nullable=False, foreign_key=True)
    product_id = Column(Integer, nullable=False, foreign_key=True)
    quantity = Column(Integer, nullable=False)