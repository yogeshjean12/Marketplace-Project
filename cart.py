from app import *


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

