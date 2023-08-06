import sqlite3 as sql

from cronably.repositories.job_repository import JobRepository
from cronably.repositories.task_repository import TaskRepository


class DbManager:

    __MY_DB_MANAGER = None
    __DB_KIND = None

    def __init__(self):
        self.__jobRepository = JobRepository(self)
        self.__taskRepository = TaskRepository(self)
        self.__db_was_configured = False
        self.__db = None
        self.init_db()

    def init_db(self):
        self.__create_db(self.__DB_KIND)
        self.__create_main_tables()
        self.__db_was_configured = True


    def __create_db(self, db_kind):
        self.__db = sql.connect(db_kind)

    def __create_main_tables(self):
        self.create_table("JOBS", [('id', 'integer', 'PRIMARY KEY ASC'), ('name', 'text', 'NOT NULL'), ('should_run', 'integer'), ('loops', 'integer'), ('report', 'integer')])
        self.create_table("TASKS", [
            ('id', 'integer', 'PRIMARY KEY ASC'),
            ('id_job', 'integer', 'NOT NULL'),
            ('start', 'text'),
            ('end', 'text'),
            ('status', 'integer'),
            ('msg', 'text'),
            ('FOREIGN', 'KEY(id_job)', 'REFERENCES JOBS(id)'),
        ])

    def is_active_db(self):
        return self.__db is not None

    def create_table(self, table_name, fields):
        field_list = '('
        for field in fields:
            field_list += field[0] + ' ' + field[1]
            if len(field) > 2:
                field_list += ' ' + field[2]

            if not field[0] == fields[len(fields) - 1][0]:
                field_list += ','
        field_list += ')'
        self.__db.execute('CREATE TABLE ' + table_name + field_list)
        self.__db.commit()

    def should_run(self, job_name):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__MY_DB_MANAGER:
            cls.__MY_DB_MANAGER = DbManager()
        return cls.__MY_DB_MANAGER

    @classmethod
    def reboot(cls):
        manager = cls.__MY_DB_MANAGER
        if manager and  manager.__db:
            manager.__db.close()
            manager.__db_was_configured = False
        cls.__MY_DB_MANAGER = None


    def get_job_repository(self):
        return self.__jobRepository

    def get_task_repository(self):
        return self.__taskRepository

    def get_db(self):
        return self.__db

    @classmethod
    def configure_db(cls, db_kind = ':memory:'):
        cls.__DB_KIND = db_kind
