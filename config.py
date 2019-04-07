from dotenv import load_dotenv
import os 

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class TestConfig(object):
    DB_NAME         = os.getenv('TEST_DB_NAME')
    DB_PASSWORD     = os.getenv('TEST_DB_PASSWORD')
    DB_USER         = os.getenv('TEST_DB_USER')
    DB_PORT         = os.getenv('TEST_DB_PORT')

class ProductionConfig(object):
    DB_NAME     = os.getenv('DB_NAME')
    DB_USER     = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT     = os.getenv('DB_PORT')
