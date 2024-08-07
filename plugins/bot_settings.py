import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv
from info import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

default_values = {
    'SESSION ': 'TechVJBot',
    'TechVJBot': 1800,
    'PICS ': 'https://graph.org/file/ce1723991756e48c35aa1.jpg',
    'NOR_IMG': 'https://graph.org/file/b69af2db776e4e85d21ec.jpg',
    'MELCOW_VID ': 'https://t.me/How_To_Open_Linkl',
    'SPELL_IMG ': 'https://te.legra.ph/file/15c1ad448dfe472a5cbb8.jpg',
    'REQUEST_TO_JOIN_MODE ': False,
    'AUTH_CHANNEL': '',
    'REQST_CHANNEL': '',
    'SUPPORT_CHAT_ID ': '',
    'PREMIUM_AND_REFERAL_MODE': False,

}
bool_vars = [
    'PREMIUM_AND_REFERAL_MODE ',
    'REQUEST_TO_JOIN_MODE ',
    'CLONE_MODE',
    'AI_SPELL_CHECK',
    'PM_SEARCH',
    'IS_SHORTLINK',
    'MAX_BTN',
    'IS_TUTORIAL',
    'P_TTI_SHOW_OFF',
    'IMDB',
    'AUTO_FFILTER',
    'AUTO_DELETE',
    'SINGLE_BUTTON',
    'LONG_IMDB_DESCRIPTION',
    'SPELL_CHECK_REPLY',
    'MELCOW_NEW_USERS',
    'PROTECT_CONTENT',
    'PUBLIC_FILE_STORE',
    'NO_RESULTS_MSG',
    'USE_CAPTION_FILTER',
    'VERIFY',
    'VERIFY_SECOND_SHORTNER',
    'SHORTLINK_MODE',
    'STREAM_MODE',
    'MULTI_CLIENT',
    'RENAME_MODE',
    'AUTO_APPROVE_MODE'
]

class DatabaseConfig:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._client is None:
            try:
                mongo_uri = os.getenv("DATABASE_URI")
                if mongo_uri is None:
                    raise Exception("DATABASE_URI is not set in environment variables")
                cls._client = MongoClient(mongo_uri)
                cls._db = cls._client.get_database("Iron")
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
                cls._db = None
        return cls._db

def create_configs_collection():
    client = MongoClient(os.getenv("DATABASE_URI"))
    db = client.get_database("Iron")

    # Check if the "configs" collection exists, and create it if not
    if "configs" not in db.list_collection_names():
        logger.info("Creating 'configs' collection...")
        db.create_collection("configs")

def load_vars():
    if not os.environ.get('ADMINS'):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../config.env')
        if not os.path.exists(dotenv_path):
            logger.error("config.env file not found")
            return
        load_dotenv(dotenv_path)
        store_var_mongo()
    store_var_mongo()

def store_var_mongo():

    env_vars = {      
             'ADMINS': ADMINS,
             'AI_SPELL_CHECK': AI_SPELL_CHECK,
             'API_HASH': API_HASH,
             'API_ID': API_ID,
             'AUTH_CHANNEL': AUTH_CHANNEL,
             'AUTH_USERS': AUTH_USERS,
             'AUTO_FFILTER': AUTO_FFILTER,
             'AUTO_DELETE': AUTO_DELETE,
             'AUTO_APPROVE_MODE': AUTO_APPROVE_MODE,
             'BOT_TOKEN': BOT_TOKEN,
             'BATCH_FILE_CAPTION': BATCH_FILE_CAPTION,
             'CACHE_TIME': CACHE_TIME,
             'CHANNELS': CHANNELS,
             'CHNL_LNK': CHNL_LNK,
             'CUSTOM_FILE_CAPTION': CUSTOM_FILE_CAPTION,
             'CLONE_MODE': CLONE_MODE,
             'CLONE_DATABASE_URI': CLONE_DATABASE_URI,
             'COLLECTION_NAME': COLLECTION_NAME,
             'DATABASE_URI': DATABASE_URI,
             'DATABASE_NAME': DATABASE_NAME,
             'DELETE_CHANNELS': DELETE_CHANNELS,
             'FILE_STORE_CHANNEL': FILE_STORE_CHANNEL,
             'GRP_LNK': GRP_LNK,
             'INDEX_REQ_CHANNEL': INDEX_REQ_CHANNEL,
             'IS_SHORTLINK': IS_SHORTLINK,
             'IS_TUTORIAL': IS_TUTORIAL,
             'IMDB': IMDB,
             'LONG_IMDB_DESCRIPTION': LONG_IMDB_DESCRIPTION,
             'IMDB_TEMPLATE': IMDB_TEMPLATE,
             'LOG_CHANNEL': LOG_CHANNEL,
             'MAX_BTN': MAX_BTN,
             'MAX_B_TN': MAX_B_TN,
             'MAX_LIST_ELM': MAX_LIST_ELM,
             'MELCOW_VID': MELCOW_VID,
             'MELCOW_NEW_USERS': MELCOW_NEW_USERS,
             'MSG_ALRT': MSG_ALRT,
             'MULTI_CLIENT': MULTI_CLIENT,
             'NOR_IMG': NOR_IMG,
             'NO_RESULTS_MSG': NO_RESULTS_MSG,
             'OWNER_USERNAME': OWNER_USERNAME,
             'PICS': PICS,
             'PING_INTERVAL': PING_INTERVAL,
             'PUBLIC_FILE_CHANNEL': PUBLIC_FILE_CHANNEL,
             'PM_SEARCH': PM_SEARCH,
             'PORT': PORT,
             'P_TTI_SHOW_OFF': P_TTI_SHOW_OFF,
             'PROTECT_CONTENT': PROTECT_CONTENT,
             'PUBLIC_FILE_STORE': PUBLIC_FILE_STORE,
             'PAYMENT_QR': PAYMENT_QR,
             'PREMIUM_AND_REFERAL_MODE': PREMIUM_AND_REFERAL_MODE,
             'REFERAL_COUNT': REFERAL_COUNT,
             'REFERAL_PREMEIUM_TIME': REFERAL_PREMEIUM_TIME,
             'REQST_CHANNEL': REQST_CHANNEL,
             'REQUEST_TO_JOIN_MODE': REQUEST_TO_JOIN_MODE,
             'RENAME_MODE': RENAME_MODE,
             'SHORTLINK_MODE': SHORTLINK_MODE,
             'SHORTLINK_URL': SHORTLINK_URL,
             'SHORTLINK_API': SHORTLINK_API,
             'SINGLE_BUTTON': SINGLE_BUTTON,
             'SPELL_IMG': SPELL_IMG,
             'SPELL_CHECK_REPLY': SPELL_CHECK_REPLY,
             'SUPPORT_CHAT': SUPPORT_CHAT,
             'STREAM_MODE': STREAM_MODE,
             'SLEEP_THRESHOLD': SLEEP_THRESHOLD,
             'TRY_AGAIN_BTN': TRY_AGAIN_BTN,
             'TUTORIAL': TUTORIAL,
             'URL': URL,
             'USE_CAPTION_FILTER': USE_CAPTION_FILTER,
             'VERIFY': VERIFY,
             'VERIFY_SHORTLINK_URL': VERIFY_SHORTLINK_URL,
             'VERIFY_SHORTLINK_API': VERIFY_SHORTLINK_API,
             'VERIFY_SECOND_SHORTNER': VERIFY_SECOND_SHORTNER,
             'VERIFY_SND_SHORTLINK_URL': VERIFY_SND_SHORTLINK_URL,
             'VERIFY_SND_SHORTLINK_API': VERIFY_SND_SHORTLINK_API,
             'VERIFY_TUTORIAL': VERIFY_TUTORIAL
    }

    create_configs_collection() 

    client = MongoClient(os.getenv("DATABASE_URI"))
    db = client.get_database("Iron")
    configs_collection = db["configs"]

    for key, value in env_vars.items():
        if configs_collection.count_documents({"key": key}) == 0:
            configs_collection.insert_one({"key": key, "value": value})
        else:
            logger.info(f"Skipping {key} as it already exists in the database.")

    logger.info("Environment variables have been checked and updated in MongoDB.")