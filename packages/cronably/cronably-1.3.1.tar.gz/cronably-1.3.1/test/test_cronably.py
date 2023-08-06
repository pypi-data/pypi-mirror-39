import os
import subprocess as sb
import unittest

from resources.example_01 import my_process
from resources.example_03 import my_process_from_file
from resources.example_04 import my_process_with_repetitions_minutes
from cronably.cronably_main import exist_job
from cronably.repositories.db_manager import DbManager
from test.my_test_case import MyTestCase


class TestCronably(MyTestCase):

    run_test_01 = ['python', '../resources/example_01.py']
    run_test_01_01 = ['python', '../resources/example_01.py']
    run_test_02 = ['python', '../resources/example_02.py']
    file_logger = 'result.txt'

    def test_black_box_evaluate_name(self):
        my_process()
        self.assertTrue(exist_job("HOLA_MUNDO"))

    def test_black_box_evaluate_from_file(self):
        values = {'name': 'HOLA_MUNDO'}
        self.setup_conf_file(values)
        my_process_from_file()
        self.assertTrue(exist_job("HOLA_MUNDO"))

    @unittest.skip("Proceso largo. cada 1 minuto dos veces")
    def test_black_box_from_file_every_minute(self):
        values = {'name': 'HOLA_MUNDO', 'repetition':{'frame':'MINUTES','period':1} , 'loops':2}
        self.setup_conf_file(values)
        my_process_from_file()
        self.assertTrue(exist_job("HOLA_MUNDO"))
        self.assertTrue(os.path.exists('./cronably_report.txt'))

    def test_black_box_for_reports(self):
        values = {'name': 'HOLA_MUNDO', 'repetition':{'frame':'SECONDS','period':1} , 'loops':2, 'report':'Y'}
        self.setup_conf_file(values)
        my_process_from_file()
        self.assertTrue(exist_job("HOLA_MUNDO"))

    @unittest.skip("Proceso largo.")
    def test_black_box_from_file_every_monday_at_10(self):
        values = {'name': 'HOLA_MUNDO', 'repetition':{'frame':'WEEKLY','period':{'day':'Monday','time':'10:00'}} }
        self.setup_conf_file(values)
        my_process_from_file()
        self.assertTrue(exist_job("HOLA_MUNDO"))

    @unittest.skip("Proceso que corre dos veces , cada 1 minuto")
    def test_black_box_every_minute(self):
        my_process_with_repetitions_minutes()
        self.assertTrue(exist_job("PROCESS_01"))

    @unittest.skip("WIP")
    def test_black_box_02(self):
        run_test = self.run_test_02[:]
        stdout = self.run_process(run_test)
        self.assertEqual(3, len(stdout))
        self.assertEqual("pre-actions started", stdout[0].strip())
        self.assertEqual("Hola Mundo", stdout[1].strip())
        self.assertEqual("post actions", stdout[2].strip())


    def run_process(self, run_test):
        with open(self.file_logger, "w") as res:
            sb.call(run_test, stdout=res)
        with open(self.file_logger, "r") as res:
            stdout = res.readlines()
        return stdout

    def tearDown(self):
        DbManager.get_instance().reboot()
        self.remove(self.file_logger)
        self.remove(self.cronably_file)
        self.remove('./cronably_report.txt')



