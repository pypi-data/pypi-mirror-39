from cronably.actions.main_action.main_action import MainAction
from cronably.repositories.db_manager import DbManager


class Context:

    def __init__(self, post_action):
        self.post_action = post_action
        self.__db_manager = DbManager.get_instance()
        self.__jobRepository = self.__db_manager.get_job_repository()
        self.__taskRepository = self.__db_manager.get_task_repository()

    def execute(self, action, repetion = None):
        loops = 0
        job = self.get_job(self.get_job_name())
        should_run = job.should_run
        while should_run:
            should_run, loops = self.task_execution(action, loops, repetion)

    def task_execution(self, action, loops, repetion):
        should_run = True
        job = self.get_job(self.get_job_name())
        was_executed = self.execute_main_action(action, job, repetion)
        if was_executed:
            loops += 1
            if loops == job.loops:
                should_run = False
        should_run &= job.should_run
        return should_run, loops

    def execute_main_action(self, action, job, repetition):
        main_action = MainAction(action, job, self.post_action)
        if repetition:
            has_run = repetition.run_action(main_action)
        else:
            has_run = main_action.run()
        return has_run

    def check_exist_job(self, name):
        return self.get_job(name)

    def get_job(self, name):
        if name:
            return self.__jobRepository.find_by_attribute('NAME', name.upper())

    def is_db_active(self):
        return self.__db_manager.is_active_db()

    def is_started(self, job_name):
        return self.get_job(job_name).should_run

    def get_last_task(self, id_job):
        return self.__taskRepository.get_last_task(id_job)

    def get_job_name(self):
        return self.post_action.processed_parameters['name']


