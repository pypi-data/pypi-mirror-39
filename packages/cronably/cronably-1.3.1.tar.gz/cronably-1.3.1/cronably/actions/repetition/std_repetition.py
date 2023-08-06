from datetime import timedelta
from cronably.actions.repetition.base_repetition import BaseRepetition


class StdRepetition(BaseRepetition):

    def __init__(self, kind, period):
        super(StdRepetition,self).__init__()
        self.last_time_run = self.get_now()
        self.next_time_run = self.last_time_run
        self.kind = kind
        self.incremental_stuff = self.create_incremental_stuff(period)

    def run_action(self, main_action):
        has_run = False
        if self.last_time_run == self.next_time_run:
            main_action.run()
            self.update_next_time_run()
            has_run = True
        elif self.should_it_run_now():
            has_run = self.common_run(main_action)
        return has_run

    def update_next_time_run(self):
        self.next_time_run = self.get_now() + self.incremental_stuff[self.kind]

    def create_incremental_stuff(self, period):
        return {
            'SECONDS':timedelta(seconds=int(period)),
            'MINUTES':timedelta(minutes=int(period)),
            'HOURS':timedelta(hours=int(period)),
            'DAYS':timedelta(days=int(period))
        }

