from datetime import datetime

from cronably.model.task import Task
from cronably.repositories.db_manager import DbManager


class MainAction:

    def __init__(self, action, job):
        self.job = job
        self.__action = action
        self.__db_manager = DbManager.get_instance()
        self.__jobRepository = self.__db_manager.get_job_repository()
        self.__taskRepository = self.__db_manager.get_task_repository()

    def run(self):
        print "......Runing Main Action"
        id_process = 0
        try:
            id_process=self._persist_start_process()
            self.__action()
            self._persist_end_process(id_process)
        except Exception as ex:
            print (str(ex))
            self._persist_end_process(id_process, 0, str(ex))
            return False
        return True

    def _persist_start_process(self):
        max_id = self._get_max_task_id()
        id_ = max_id + 1
        start = datetime.now().strftime("%Y/%m/%dT%H:%M:%S")
        task = Task(id_, self.job.id , start)
        return self.__taskRepository.create(task)

    def _get_max_task_id(self):
        return self.__taskRepository.get_max_task_id()

    def _persist_end_process(self, id_process, status = 1, msg = None):
        self.__taskRepository.update_end(id_process, status, msg)