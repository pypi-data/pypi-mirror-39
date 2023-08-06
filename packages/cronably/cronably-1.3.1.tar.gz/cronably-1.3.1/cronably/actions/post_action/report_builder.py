from string import Template

from cronably.repositories.db_manager import DbManager


class ReportBuilder:

    def __init__(self, params, process_log):
        print '## Report'
        self.params = params
        self.process_log = process_log
        self.__db_manager = DbManager.get_instance()
        self.__jobRepository = self.__db_manager.get_job_repository()
        self.__taskRepository = self.__db_manager.get_task_repository()

    def build(self):
        job = self.__jobRepository.get_last_JOB()
        template_job = self.init_template_for_job(job)
        template_params = self.append_params()
        template_task = self.complete_template_for_task(job)
        with open('cronably_report.txt', 'w') as cronably_file:
            cronably_file.write(template_job)
            cronably_file.write(template_params)
            cronably_file.write(template_task)

    def init_template_for_job(self, job):
        value ="""Job\njob_id: $job_id\njob_name: $job_name\nloops_setted: $job_loops\n-------------------------------------------\n"""
        template = Template(value)
        value = template.safe_substitute({'job_id':job.id, 'job_name': job.name, '$job_loops': job.loops})
        return value

    def append_params(self):
        params = "Params\n"
        for key, val in self.params.items():
            params += "%s:%s\n" % (str(key), str(val))
        params += "-------------------------------------------\n"
        return params

    def complete_template_for_task(self, job):
        tasks = self.__taskRepository.find_all_by_job_id(job.id)
        template = "TASKS\n"
        template += "-------------------------------------------\n"
        for task in tasks:
            template += self.get_task_id_val(task)
            template += self.get_start_val(task)
            template += self.get_end_val(task)
            template += self.get_status_val(task)
            template += self.get_out_val(task)
            template += "-------------------------------------------\n"
        return template


    def get_task_id_val(self, task):
        return "task: %s\n" % str(task.id)

    def get_start_val(self, task):
        return "start: %s\n" % str(task.start)

    def get_end_val(self, task):
        return "end: %s\n" % str(task.end)

    def get_status_val(self, task):
        return "status: %s\n" % str(task.status)

    def get_out_val(self, task):
        out = "output:\n"
        for proc_log in self.process_log[task.id]:
            out += proc_log + '\n'
        return out
