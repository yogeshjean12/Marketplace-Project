from app import *


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    image = Column(String)

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
        category_dict['category_image'] = _category.image
        return category_dict

