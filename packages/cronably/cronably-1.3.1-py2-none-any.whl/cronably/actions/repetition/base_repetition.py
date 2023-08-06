from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta


class BaseRepetition:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run_action(self, main_action):
        pass

    def common_run(self, main_action):
        try:
            main_action.run()
            self.last_time_run = self.next_time_run
            self.update_next_time_run()
            return True
        except Exception as ex:
            print(str(ex))
            return False

    @abstractmethod
    def update_next_time_run(self):
        pass

    def should_it_run_now(self):
        return self.next_time_run - self.get_now() <= timedelta(seconds=0)

    def get_now(self):
        return datetime.now()


