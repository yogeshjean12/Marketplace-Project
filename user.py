from app import *


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
        if _user is not None:
            if _user.user_name == self._user_name and _user.password == self._password:
                return True
            else:
                return False
        else:
            return False

    def get_user_id(self):
        _user = db_session.query(User).filter_by(user_name=self._user_name).first()
        return _user.user_id

    def register_user(self, confirm_password):
        if self.__is_username_exist() == False and self.__is_password_valid(confirm_password) == True:
            db.execute('insert into users '
                    'values(\'{}\',\'{}\',\'{}\')'.format(self.__get_new_id(), self._user_name, self._password))
            return True
        else:
            return False

    def __is_username_exist(self):
        _user = db_session.query(User).filter_by(user_name=self._user_name).first()
        if _user is None:
            return False
        else:
            return True


    def __is_password_valid(self, confirm_password):
        if self._password == confirm_password:
            if self._password != '' and confirm_password != '':
                return True
            else:
                return False
        else:
            return False



    def __get_new_id(self):
        id = db.execute('select max(user_id) from users')
        new_id = (id.fetchone()[0]) + 1
        return new_id
