from datetime import timedelta, datetime
from cronably.actions.repetition.base_repetition import BaseRepetition


class WeeklyRepetition(BaseRepetition):

    def __init__(self, day, time):
        super(WeeklyRepetition, self).__init__()
        self.day = day.upper()
        self.time = time
        self.next_time_run = None
        self.last_time_run = None

    def update_next_time_run(self):
        time = self.time.split(':')
        day= self.get_name_day_for_today(self.get_now()).upper()
        if self.day == day:
            self.next_time_run = self.get_now()
            if self.is_overtimed(self.next_time_run):
                self.next_time_run = self.update_by(7, time)
            else:
                self.next_time_run = self.update_by(0, time)
        else:
            for day_diff in range(1,7):
                if self.difference_betwween_days(day_diff):
                    self.next_time_run = self.update_by(day_diff, time)
                    break

    def get_name_day_for_today(self, date_val):
        return date_val.strftime('%A').upper()

    def run_action(self, main_action):
        has_run = False
        if self.should_it_run_now():
            has_run = self.common_run(main_action)
        return has_run

    def is_overtimed(self, date_to_check):
        time = self.time.split(':')
        hour = date_to_check.hour
        minute = date_to_check.minute
        if hour > int(time[0]):
            return True
        else:
            if hour == int(time[0]):
                if minute >= int(time[1]):
                    return True
        return False

    def update_by(self, amount_days, time):
        next_val= self.get_now() + timedelta(days=amount_days)
        year =next_val.year
        month = next_val.month
        day = next_val.day
        return datetime(year, month, day, int(time[0]), int(time[1]), 0)

    def difference_betwween_days(self, days):
        now = self.get_now() + timedelta(days=days)
        return self.get_name_day_for_today(now) == self.day
