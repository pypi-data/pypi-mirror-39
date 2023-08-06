from abc import ABCMeta, abstractmethod


class Repository:
    __metaclass__ = ABCMeta

    def __init__(self, db_manager):
        self.__db_manager = db_manager

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_attribute(self, field, att):
        pass

    @abstractmethod
    def delete_by_id(self, id):
        pass

    @abstractmethod
    def create(self, model):
        pass

    @abstractmethod
    def update(self, model):
        pass

    def execute_select_one(self, query, value = None):
        if value:
            return  self.get_db().execute(query, value).fetchone()
        else:
            return self.get_db().execute(query).fetchone()

    def execute_select_all(self, query, value = None):
        if value:
            return  self.get_db().execute(query, value).fetchall()
        else:
            return self.get_db().execute(query).fetchall()


    def do_action(self, param, insert_or_update):
        value = self.get_db().execute(insert_or_update, param).lastrowid
        self.get_db().commit()
        return value

    def get_db(self):
        return self.__db_manager.get_db()