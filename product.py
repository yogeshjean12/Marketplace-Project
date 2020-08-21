from app import *
from category import *
from seller import *


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

