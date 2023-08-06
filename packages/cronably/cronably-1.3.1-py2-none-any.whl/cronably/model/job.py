

class Job:

    def __init__(self, id, name, should_run=True, loops=1, report = False):
        self.id = id
        self.name = name
        self.should_run = should_run
        self.loops = loops
        self.report = report

    @staticmethod
    def create_from_query(param):
        if param:
            return Job(param[0], param[1], param[2], param[3], param[4])

    @classmethod
    def create_job_from_params(cls, parameters):
        loops = Job._check_param(parameters, "loops", 1)
        report = 1 if Job._check_param(parameters, "report", "n").lower() == "y" else 0
        return Job(-1, parameters['name'], True, loops, report)

    @staticmethod
    def _check_param(parameters,  param, default):
        if param in parameters.keys():
            return parameters[param]
        return default
