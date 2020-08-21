from app import *


class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, seller_id):
        self._seller_id = seller_id

    def get_seller_name(self):
        _seller = db_session.query(Seller).filter_by(id=self._seller_id).first()
        return _seller.name
