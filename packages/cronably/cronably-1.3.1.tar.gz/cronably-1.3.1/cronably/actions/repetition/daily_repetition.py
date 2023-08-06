from datetime import timedelta

from cronably.actions.repetition.base_repetition import BaseRepetition


class DailyRepetition(BaseRepetition):

    def __init__(self, schedule):
        super(DailyRepetition, self).__init__()
        self.schedules = schedule.split(',')
        self.initialize_last_time()
        self.update_next_time_run()

    def initialize_last_time(self):
        time = self.schedules[len(self.schedules) - 1]
        self.last_time_run = self.adjust_day_with_time(time, -1)

    def update_next_time_run(self):
        size_schedule = len(self.schedules)
        configured = self.evaluate_now_before_adjust_position(0)
        if not configured and size_schedule > 1:
            for x in range(size_schedule):
                configured = self.evaluate_config(x, x + 1)
                if x + 2 == size_schedule and not configured:
                    break

        if not configured:
            self.next_time_run = self.adjust_day_with_time(self.schedules[0], 1)

    def evaluate_config(self, base, next_val):
        configured = self.evaluate_now_before_adjust_position(base)
        if not configured:
            configured = self.evaluate_now_before_adjust_position(next_val)
        return configured

    def evaluate_now_before_adjust_position(self, position):
        configured = False
        configured_run = self.adjust_day_with_time(self.schedules[position])
        if self.get_now() < configured_run:
            self.next_time_run = configured_run
            configured = True
        return configured

    def run_action(self, main_action):
        has_run = False
        if self.should_it_run_now():
            has_run = self.common_run(main_action)
        return has_run

    def adjust_day_with_time(self, time, param = 0):
        time_splt = time.split(':')
        result = self.get_now().replace(hour=int(time_splt[0]), minute=int(time_splt[1]), second=0)
        return result + timedelta(days=param)







