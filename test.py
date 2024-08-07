import logging
import os
from dotenv import load_dotenv
from logging import  error as log_error

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
ADMINS = os.environ.get('ADMINS', '')
if ADMINS == "":
    ADMINS = ''

def store_var_mongo():
    print("store_var_mongo bbbbbb")

def load_vars():
    if not ADMINS:
        dotenv_path = os.path.join(os.path.dirname(__file__), '../config.env')
        if not os.path.exists(dotenv_path):
            log_error("config.env file not found")
            return
        load_dotenv(dotenv_path)
        store_var_mongo()
    store_var_mongo()

main = load_vars()

print(main)