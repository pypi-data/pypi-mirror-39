from cronably.model.job import Job
from cronably.repositories.repository import Repository


class JobRepository(Repository):

    def __init__(self, db_manager):
        super(JobRepository, self).__init__(db_manager)

    def find_by_id(self, id):
        pass

    def find_all(self):
        pass

    def find_by_attribute(self,field,  att):
        query = """ SELECT * FROM JOBS WHERE %s = ?""" % field
        name = (att,)
        result = Job.create_from_query(self.execute_select_one(query, name))
        return result

    def delete_by_id(self, id):
        pass

    def create(self, job):
        insert = '''INSERT INTO JOBS('id','name', 'should_run', 'loops', 'report') VALUES ( ?, ?, ?, ?, ?) '''
        should_run = 1 if job.should_run else 0
        last_job = self.get_last_JOB()
        last_id = 1 if not last_job else last_job.id + 1
        self.do_action((last_id, job.name.upper(), should_run, job.loops, job.report), insert)

    def stop_job(self, job_id):
        update = '''UPDATE JOBS SET should_run=0 WHERE ID = ?'''
        self.do_action((job_id,), update)

    def start_job(self, job_id):
        update = '''UPDATE JOBS SET should_run=1 WHERE ID = ?'''
        self.do_action((job_id,), update)

    def update(self, model):
        pass

    def get_last_JOB(self):
        query = """ SELECT * FROM JOBS ORDER BY ID desc LIMIT 1"""
        result = Job.create_from_query(self.execute_select_one(query))
        return result
