from cronably.actions.pre_action.parameters import Parameters
from cronably.actions.pre_action.pre_action_validations import PreActionValidations
from cronably.actions.repetition.repetition_factory import RepetitionFactory
from cronably.model.job import Job
from cronably.repositories.db_manager import DbManager


class PreActions:

    def __init__(self, atts = {}):
        print '-------------'
        print '# PreActions'
        self.processed_parameters = Parameters(atts).build()
        self.load_from_file = False
        print '## Validations'
        validations = self.init_validations()
        print '## InitDB'
        self.__job_repository = self.initialize_db()
        print '## Create Repetitions'
        self.repetition = self.create_repetition(validations)
        print '## Create Job'
        self.create_job()
        print '-------------'

    def initialize_db(self):
        DbManager.configure_db(self.processed_parameters['db_kind'])
        return  DbManager.get_instance().get_job_repository()

    def create_repetition(self, validations):
        if validations.has_repetition_strategy():
            return RepetitionFactory(self.processed_parameters).get_repetition()
        return None

    def create_job(self):
        job = Job.create_job_from_params(self.processed_parameters)
        return self.__job_repository.create(job)

    def init_validations(self):
        validations = PreActionValidations(self.processed_parameters)
        validations.run()
        return validations
