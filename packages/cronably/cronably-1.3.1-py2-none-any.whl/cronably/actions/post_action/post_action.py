from cronably.actions.post_action.report_builder import ReportBuilder
from cronably.actions.pre_action.parameters import Parameters


class PostAction:
    pass

    def __init__(self, atts = {}):
        print '-------------'
        print '# PostActions'
        self.processed_parameters = atts
        self.process_log = {}

    def save_process_info(self, id_process, output):
        self.process_log[id_process] = output

    def append_exc_to_logs(self, id_process, fail):
        output = self.process_log[id_process]
        output.append(str(fail))

    def get_output_from_id(self, id):
        return self.process_log[id]

    def should_make_report(self):
        return Parameters(self.processed_parameters).has_to_make_reports()

    def run(self):
        if self.should_make_report():
            ReportBuilder(self.processed_parameters, self.process_log).build()

