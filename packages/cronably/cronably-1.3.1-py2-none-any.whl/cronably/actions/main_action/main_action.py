from datetime import datetime

from cronably.actions.main_action.capturing import Capturing
from cronably.model.task import Task
from cronably.repositories.db_manager import DbManager


class MainAction:

    def __init__(self, action, job, post_action):
        self.job = job
        self.post_action = post_action
        self.__action = action
        self.__db_manager = DbManager.get_instance()
        self.__jobRepository = self.__db_manager.get_job_repository()
        self.__taskRepository = self.__db_manager.get_task_repository()

    def run(self):
        print "## Runing Main Action"
        id_process = 0
        try:
            id_process = self._persist_start_process()
            self.run_action(id_process)
            self._persist_end_process(id_process)
        except Exception as ex:
            print (str(ex))
            if self.should_make_report():
                self.post_action.append_exc_to_logs(id_process, ex)
            self._persist_end_process(id_process, 0, str(ex))
            return False
        return True

    def run_action(self, id_process):
        if self.should_make_report():
            self.run_action_with_reporting(id_process)
        else:
            self.__action()

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

    def should_make_report(self):
        return self.post_action.should_make_report()

    def run_action_with_reporting(self, id_process):
        output = []
        with Capturing(output) as output:  # note the constructor argument
            try:
                self.__action()
                self.post_action.save_process_info(id_process, output)
            except Exception as ex:
                self.post_action.save_process_info(id_process, output)
                raise ex