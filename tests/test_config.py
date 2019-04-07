from apitest.create_test import create_app
from apitest.config import TestConfig
from apitest.database import main
import unittest



class BaseTest(unittest.TestCase):
    """
    configurations for all the tests that will be written in the different files
    setUp contains the program that will be carried out before each of the tests begin
    tearDown contains the program that will be carried out after each of the tests has been carried out
    """

    def setUp(self):
        # setup the application that 
        main(TestConfig)
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    
    def tearDown(self):
        main(TestConfig)


