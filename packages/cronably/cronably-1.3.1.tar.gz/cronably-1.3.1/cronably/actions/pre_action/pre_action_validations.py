from cronably.utils.cronably_exception import CronablyException


class PreActionValidations(object):

    def __init__(self, params):
        self.parameters = params
        self.conf_dict_file = {'frame':'repetition.frame','period':'repetition.period', 'day':"repetition.period.day", 'time':"repetition.period.time" }
        self.conf_dict_code = {'frame':'repetition_frame','period':'repetition_period', 'day':"repetition_period_day", 'time':"repetition_period_time" }

    def run(self):
        print '### has name'
        self.job_has_name()
        print '### db kind'
        self.check_db_kind()

    def check_param(self, param, default):
        if param in self.parameters.keys():
            return self.parameters[param]
        return default

    def job_has_name(self):
        if not self.check_param('name', False):
            raise CronablyException("You should add a name into your Cronably annotation")

    def has_repetition_strategy(self):
        return self.evaluate_period_conditions(self._get_config('frame'))

    def evaluate_period_conditions(self, frame):
        period = self._get_config('period')
        day = self._get_config('day')
        time = self._get_config('time')
        ok_period = self.evaluate_day_time(period, day, time)
        return self.evaluate_repetitions(self.check_param(frame, False), ok_period, 'frame', 'period')

    def evaluate_day_time(self,period, day, time):
        if self.check_param(period, False):
            return True
        else:
            return self.evaluate_repetitions(
                self.check_param(day, False)
                , self.check_param(time, False), day, time)

    def evaluate_repetitions(self, condition_a, condition_b, parm_a, parm_b):
        only_frame = condition_a and not condition_b
        only_period = not condition_a and condition_b
        if not condition_a and not condition_b:
            return False
        elif only_frame or only_period:
            raise CronablyException('Repetition miss params, check you add %s and %s' % (parm_a, parm_b))
        else:
            return True

    def _get_config(self, param):
        if self.check_param("ext_config", False):
            return self.conf_dict_file[param]
        else:
            return self.conf_dict_code[param]

    def check_db_kind(self):
        if not self.check_param('db_kind', False):
            self.parameters['db_kind'] = 'cronably' if self.check_param('db_kind', False) else ':memory:'
        else:
            value = self.parameters['db_kind']
            self.parameters['db_kind'] = ':memory:' if value=='memory' else self.parameters['db_kind']
