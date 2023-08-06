from cronably.actions.repetition.daily_repetition import DailyRepetition
from cronably.actions.repetition.std_repetition import StdRepetition
from cronably.actions.repetition.weekly_repetition import WeeklyRepetition


class RepetitionFactory:

    def __init__(self, parameters):
        self.processed_parameters = parameters

    def get_repetition(self):
        if self._get_frame() == 'DAILY':
            return self._create_daily_repetition()
        if self._get_frame() == 'WEEKLY':
            return self._create_weekly_repetition()
        else:
            return StdRepetition(self._get_frame(), self._get_period())

    def _create_weekly_repetition(self):
        repetition = WeeklyRepetition(self._get_day(), self._get_time())
        repetition.update_next_time_run()
        return repetition

    def _create_daily_repetition(self):
        repetition = DailyRepetition(self._get_value_according_config_source('period'))
        return repetition

    def _check_frame(self, frame):
        return self._get_frame() == frame

    def _get_period(self):
        return self._get_value_according_config_source('period')

    def _get_frame(self):
        frame = self._get_value_according_config_source('frame')
        return frame.upper()

    def _get_value_according_config_source(self, value):
        if self._check_param('ext_config', False):
            return self.processed_parameters['repetition.%s' % value]
        else:
            return self.processed_parameters['repetition_%s' % value]

    def _get_day(self):
        day = 'period.day' if self._check_param('ext_config', False) else 'period_day'
        return self._get_value_according_config_source(day)

    def _get_time(self):
        time = 'period.time' if self._check_param('ext_config', False) else 'period_time'
        return self._get_value_according_config_source(time)

    def _check_param(self, param, default):
        if param in self.processed_parameters.keys():
            return self.processed_parameters[param]
        return default

