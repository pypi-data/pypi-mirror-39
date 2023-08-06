from datetime import datetime

from cronably.model.task import Task
from cronably.repositories.repository import Repository


class TaskRepository(Repository):

    def __init__(self, (db_manager)):
        super(TaskRepository, self).__init__(db_manager)

    def find_by_id(self, id):
        pass

    def find_all(self):
        pass

    def find_by_attribute(self, att):
        pass

    def delete_by_id(self, id):
        pass

    def create(self, task):
        insert = '''INSERT INTO TASKS('id','id_job', 'start') VALUES ( ?, ?, ?) '''
        return self.do_action((task.id, task.id_job, task.start), insert)

    def update(self, model):
        pass

    def update_end(self, id_process, status, msg):
        insert = '''UPDATE TASKS SET end = ?, status = ?, msg = ? where id = ? '''
        end = datetime.now().strftime("%Y/%m/%dT%H:%M:%S")
        self.do_action((end, status, msg, id_process), insert)

    def get_last_task(self, id_job):
        query = """ SELECT * FROM TASKS WHERE ID_JOB = ? ORDER BY START desc LIMIT 1"""
        name = (id_job,)
        result = Task.create_from_query(self.execute_select_one(query, name))
        return result

    def get_max_task_id(self):
        query = """SELECT MAX(ID) FROM TASKS """
        result = self.execute_select_one(query)
        return 1 if not result[0] else result[0]

    def find_all_by_job_id(self, job_id):
        query = """ SELECT * FROM TASKS WHERE ID_JOB = ? ORDER BY START"""
        name = (job_id,)
        result = Task.create_from_query_all(self.execute_select_all(query, name))
        return result