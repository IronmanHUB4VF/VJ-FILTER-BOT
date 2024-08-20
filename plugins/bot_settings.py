import re, asyncio

from pyrogram import Client,filters
from logging import getLogger, ERROR
from random import choice
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message
from pyrogram.filters import command, regex, create
from pyrogram.enums import ChatType, ParseMode
from pyrogram.errors import ReplyMarkupInvalid, FloodWait, PeerIdInvalid, ChannelInvalid, RPCError, UserNotParticipant, MessageNotModified, MessageEmpty, PhotoInvalidDimensions, WebpageCurlFailed, MediaEmpty
from functools import partial, wraps
from collections import OrderedDict
from asyncio import create_subprocess_exec, create_subprocess_shell, sleep, gather, run_coroutine_threadsafe
from aiofiles.os import remove, rename, path as aiopath
from aiofiles import open as aiopen
from os import environ, getcwd
from dotenv import load_dotenv
from time import time
from io import BytesIO
from dotenv import dotenv_values
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient
from traceback import format_exc

from Config import config_dict, DATABASE_URI, download_dict, status_reply_dict_lock, Interval, bot_id, ADMINS
from Script import script


getLogger("pyrogram").setLevel(ERROR)
getLogger("aiohttp").setLevel(ERROR)
getLogger("httpx").setLevel(ERROR)

LOGGER = getLogger(__name__)

START = 0
STATE = 'view'
handler_dict = {}
id_pattern = re.compile(r'^.\d+$')
#loop = asyncio.get_event_loop()

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

bset_display_dict = {'AUTH_CHANNEL': 'Fill chat_id(-100xxxxxx) of groups/channel you want to force subscribe. Separate them by space. Int\n\nNote: Bot should be added in the filled chat_id as admin',
                'BOT_TOKEN': 'The Telegram Bot Token that you got from @BotFather',
                'CMD_SUFFIX': 'Telegram Bot Command Index number or Custom Text. This will added at the end all commands except Global Commands. Str',
                'DATABASE_URI': "Your Mongo Database URL (Connection string). Follow this Generate Database to generate database. Data will be saved in Database: auth and sudo users, users settings including thumbnails for each user, rss data and incomplete tasks.\n\n <b>NOTE:</b> You can always edit all settings that saved in database from the official site -> (Browse collections)",
                'API_ID': 'This is to authenticate your Telegram account for downloading Telegram files. You can get this from https://my.telegram.org.',
                'API_HASH': 'This is to authenticate your Telegram account for downloading Telegram files. You can get this from https://my.telegram.org.',
}

class DbManager:
    def __init__(self):
        self.__err = False
        self.__db = None
        self.__conn = None
        self.__connect()

    def __connect(self):
        try:
            self.__conn = AsyncIOMotorClient(DATABASE_URI)
            self.__db = self.__conn.luna
        except PyMongoError as e:
            LOGGER.error(f"Error in DB connection: {e}")
            self.__err = True

    async def db_load(self):
        if self.__err:
            return
        await self.__db.settings.config.update_one(
            {"_id": bot_id}, {"$set": config_dict}, upsert=True
        )
        self.__conn.close

    async def update_config(self, dict_):
        if self.__err:
            return
        await self.__db.settings.config.update_one(
            {"_id": bot_id}, {"$set": dict_}, upsert=True
        )
        self.__conn.close

if DATABASE_URI:
    async def db_loder():
        await DbManager().db_load()


async def load_config():

    BOT_TOKEN = environ.get('BOT_TOKEN', '')
    if len(BOT_TOKEN) == 0:
        BOT_TOKEN = config_dict['BOT_TOKEN']

    API_ID = environ.get('API_ID', '')
    if len(API_ID) == 0:
        API_ID = config_dict['API_ID']
    else:
        API_ID = int(API_ID)

    API_HASH = environ.get('API_HASH', '')
    if len(API_HASH) == 0:
        API_HASH = config_dict['API_HASH']

    OWNER_ID = environ.get('OWNER_ID', '')
    OWNER_ID = config_dict['OWNER_ID'] if len(OWNER_ID) == 0 else int(OWNER_ID)

    ADMINS = environ.get('ADMINS', '')
    ADMINS = config_dict['ADMINS'] if len(ADMINS) == 0 else int(ADMINS)

    DATABASE_URI = environ.get('DATABASE_URI', '')
    if len(DATABASE_URI) == 0:
        DATABASE_URI = ''

    DATABASE_NAME = environ.get('DATABASE_NAME', '')
    if len(DATABASE_NAME) == 0:
        DATABASE_NAME = ''

    COLLECTION_NAME = environ.get('COLLECTION_NAME', '')
    if len(COLLECTION_NAME) == 0:
        COLLECTION_NAME = ''

    AUTH_USERS = environ.get('AUTH_USERS', '')
    if len(AUTH_USERS) == 0:
        AUTH_USERS = ''
    
    AUTH_CHANNEL = environ.get('AUTH_CHANNEL', '')
    if len(AUTH_CHANNEL) == 0:
        AUTH_CHANNEL = ''

    REQST_CHANNEL = environ.get('REQST_CHANNEL', '')
    if len(REQST_CHANNEL) == 0:
        REQST_CHANNEL = ''

    LOG_CHANNEL = environ.get('LOG_CHANNEL', '-1001862601820')
    LOG_CHANNEL = config_dict['LOG_CHANNEL'] if len(LOG_CHANNEL) == 0 else int(LOG_CHANNEL)

    CHANNELS = environ.get('CHANNELS', '-1001878326006 -1001895151847')
    CHANNELS = config_dict['CHANNELS'] if len(CHANNELS) == 0 else CHANNELS

    CACHE_TIME = environ.get('CACHE_TIME', "")
    if len(CACHE_TIME) == 0:
        CACHE_TIME = 1800
    else:
        CACHE_TIME = int(CACHE_TIME)

    CMD_SUFFIX = environ.get('CMD_SUFFIX', '')
    if len(CMD_SUFFIX) == 0:
        CMD_SUFFIX = ''

    PICS = environ.get('PICS', '') #SAMPLE PIC
    if len(PICS) == 0:
        PICS = 'https://graph.org/file/81b325f3e45868ee1a1cd.jpg'

    NOR_IMG = environ.get("NOR_IMG", "")
    if len(NOR_IMG) == 0:
        NOR_IMG = 'https://graph.org/file/b69af2db776e4e85d21ec.jpg'

    MELCOW_VID = environ.get("MELCOW_VID", "")
    if len(MELCOW_VID) == 0:
        MELCOW_VID = 'https://t.me/How_To_Open_Linkl'

    SPELL_IMG = environ.get("SPELL_IMG", "")
    if len(SPELL_IMG) == 0:
        SPELL_IMG = 'https://te.legra.ph/file/15c1ad448dfe472a5cbb8.jpg'

    REQUEST_TO_JOIN_MODE = environ.get('REQUEST_TO_JOIN_MODE', 'False')
    REQUEST_TO_JOIN_MODE = REQUEST_TO_JOIN_MODE.lower() == 'true'

    TRY_AGAIN_BTN = environ.get('TRY_AGAIN_BTN', 'False') # Set True Or False (This try again button is only for request to join fsub not for normal fsub)
    TRY_AGAIN_BTN = TRY_AGAIN_BTN.lower() == 'true'

    support_chat_id = environ.get('SUPPORT_CHAT_ID', '')
    SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None

    INDEX_REQ_CHANNEL = environ.get('INDEX_REQ_CHANNEL', '')
    if len(INDEX_REQ_CHANNEL) == 0:
        INDEX_REQ_CHANNEL = LOG_CHANNEL
    else:
        INDEX_REQ_CHANNEL = int(INDEX_REQ_CHANNEL)

    FILE_STORE_CHANNEL = environ.get('FILE_STORE_CHANNEL', '') #Multiple ids
    if len(FILE_STORE_CHANNEL) == 0:
        FILE_STORE_CHANNEL = ''

    DELETE_CHANNELS = environ.get('DELETE_CHANNELS', '') #MUltiple ids
    if len(DELETE_CHANNELS) == 0:
        DELETE_CHANNELS = ''

    PREMIUM_AND_REFERAL_MODE = environ.get('PREMIUM_AND_REFERAL_MODE', 'False') # Set Ture Or False
    PREMIUM_AND_REFERAL_MODE = PREMIUM_AND_REFERAL_MODE.lower() == 'true'

    REFERAL_COUNT = environ.get('REFERAL_COUNT', '') # number of referal count
    if REFERAL_COUNT == '':
        REFERAL_COUNT = 20
    else:
        REFERAL_COUNT = int(REFERAL_COUNT)

    REFERAL_PREMEIUM_TIME = environ.get('REFERAL_PREMEIUM_TIME', '')
    if REFERAL_PREMEIUM_TIME == '':
        REFERAL_PREMEIUM_TIME = '1month'

    PAYMENT_QR = environ.get('PAYMENT_QR', '')
    if PAYMENT_QR == '':
        PAYMENT_QR = 'https://graph.org/file/2a6f10c13b59cbdb091f5.jpg'

    PAYMENT_TEXT = environ.get('PAYMENT_TEXT', '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs - \n\n- 30ʀs - 1 ᴡᴇᴇᴋ\n- 50ʀs - 1 ᴍᴏɴᴛʜs\n- 120ʀs - 3 ᴍᴏɴᴛʜs\n- 220ʀs - 6 ᴍᴏɴᴛʜs\n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n✨ ᴜᴘɪ ɪᴅ - <code>jivshn@okaxis</code>\n\nᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>')
    if PAYMENT_TEXT == '':
        PAYMENT_TEXT = '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs - \n\n- 30ʀs - 1 ᴡᴇᴇᴋ\n- 50ʀs - 1 ᴍᴏɴᴛʜs\n- 120ʀs - 3 ᴍᴏɴᴛʜs\n- 220ʀs - 6 ᴍᴏɴᴛʜs\n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n✨ ᴜᴘɪ ɪᴅ - <code>jivshn@okaxis</code>\n\nᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>'

    OWNER_USERNAME = environ.get('OWNER_USERNAME', '') # owner username without @
    if OWNER_USERNAME == '': 
        OWNER_USERNAME = "LazyIron"

    # Clone Information : If Clone Mode Is True Then Bot Clone Other Bots.
    CLONE_MODE = environ.get('CLONE_MODE', 'False') # Set True or False
    CLONE_MODE = CLONE_MODE.lower() == 'true'

    CLONE_DATABASE_URI = environ.get('CLONE_DATABASE_URI', "") # Necessary If clone mode is true
    if len(CLONE_DATABASE_URI) == 0:
        CLONE_DATABASE_URI = ''
    
    PUBLIC_FILE_CHANNEL = environ.get('PUBLIC_FILE_CHANNEL', '') # Public Channel Username Without @ or without https://t.me/ and Bot Is Admin With Full Right.
    if len(PUBLIC_FILE_CHANNEL) == 0:
        PUBLIC_FILE_CHANNEL = ''

    # Links
    GRP_LNK = environ.get('GRP_LNK', '')
    if len(GRP_LNK) == 0:
        GRP_LNK = 'https://t.me/HUB4VF'

    CHNL_LNK = environ.get('CHNL_LNK', '')
    if len(CHNL_LNK) == 0:
        CHNL_LNK = 'https://t.me/HUB4VF'

    TUTORIAL = environ.get('TUTORIAL', '')
    if len(TUTORIAL) == 0:
        TUTORIAL = 'https://t.me/How_To_Open_Linkl'

    SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '') # Support Chat Link Without https:// or @
    if SUPPORT_CHAT == '':
        SUPPORT_CHAT = 'HUB4VF_Bot_Discussion'

    # True Or False
    AI_SPELL_CHECK = environ.get('AI_SPELL_CHECK', 'False')
    AI_SPELL_CHECK = AI_SPELL_CHECK.lower() == 'true'

    PM_SEARCH = environ.get('PM_SEARCH', 'False')
    PM_SEARCH = PM_SEARCH.lower() == 'true'

    IS_SHORTLINK = environ.get('IS_SHORTLINK', 'False')
    IS_SHORTLINK = IS_SHORTLINK.lower() == 'true'

    MAX_BTN = environ.get('MAX_BTN', "True")
    MAX_BTN = MAX_BTN.lower() == 'true'

    IS_TUTORIAL = environ.get('IS_TUTORIAL', 'False')
    IS_TUTORIAL = IS_TUTORIAL.lower() == 'true'

    P_TTI_SHOW_OFF = environ.get('P_TTI_SHOW_OFF', "False")
    P_TTI_SHOW_OFF = P_TTI_SHOW_OFF.lower() == 'true'

    IMDB = environ.get('IMDB', "False")
    IMDB = IMDB.lower() == 'true'

    AUTO_FFILTER = environ.get('AUTO_FFILTER', "True")
    AUTO_FFILTER = AUTO_FFILTER.lower() == 'true'

    AUTO_DELETE = environ.get('AUTO_DELETE', "True")
    AUTO_DELETE = AUTO_DELETE.lower() == 'true'

    SINGLE_BUTTON = environ.get('SINGLE_BUTTON', "True")
    SINGLE_BUTTON = SINGLE_BUTTON.lower() == 'true'

    LONG_IMDB_DESCRIPTION = environ.get("LONG_IMDB_DESCRIPTION", "False")
    LONG_IMDB_DESCRIPTION = LONG_IMDB_DESCRIPTION.lower() == 'true'

    SPELL_CHECK_REPLY = environ.get("SPELL_CHECK_REPLY", "False")
    SPELL_CHECK_REPLY = SPELL_CHECK_REPLY.lower() == 'true'

    MELCOW_NEW_USERS = environ.get('MELCOW_NEW_USERS', "True")
    MELCOW_NEW_USERS = MELCOW_NEW_USERS.lower() == 'true'

    PROTECT_CONTENT = environ.get('PROTECT_CONTENT', "False")
    PROTECT_CONTENT = PROTECT_CONTENT.lower() == 'true'

    PUBLIC_FILE_STORE = environ.get('PUBLIC_FILE_STORE', "False")
    PUBLIC_FILE_STORE = PUBLIC_FILE_STORE.lower() == 'true'

    NO_RESULTS_MSG = environ.get("NO_RESULTS_MSG", 'False')
    NO_RESULTS_MSG = NO_RESULTS_MSG.lower() == 'true'

    USE_CAPTION_FILTER = environ.get('USE_CAPTION_FILTER', 'True')
    USE_CAPTION_FILTER = USE_CAPTION_FILTER.lower() == 'true'


    # Token Verification Info :
    VERIFY = environ.get('VERIFY', 'False')
    VERIFY = VERIFY.lower() == 'true'

    VERIFY_SECOND_SHORTNER = environ.get('VERIFY_SECOND_SHORTNER', 'False')
    VERIFY_SECOND_SHORTNER = VERIFY_SECOND_SHORTNER.lower() == 'true'

    VERIFY_SHORTLINK_URL = environ.get('VERIFY_SHORTLINK_URL', '')
    if len(VERIFY_SHORTLINK_URL) == 0:
        VERIFY_SHORTLINK_URL = ''

    VERIFY_SHORTLINK_API = environ.get('VERIFY_SHORTLINK_API', '')
    if len(VERIFY_SHORTLINK_API) == 0:
        VERIFY_SHORTLINK_API = ''

    # if verify second shortner is True then fill below url and api
    VERIFY_SND_SHORTLINK_URL = environ.get('VERIFY_SND_SHORTLINK_URL', '')
    if len(VERIFY_SND_SHORTLINK_URL) == 0:
        VERIFY_SND_SHORTLINK_URL = ''

    VERIFY_SND_SHORTLINK_API = environ.get('VERIFY_SND_SHORTLINK_API', '')
    if len(VERIFY_SND_SHORTLINK_API) == 0:
        VERIFY_SND_SHORTLINK_API = ''

    VERIFY_TUTORIAL = environ.get('VERIFY_TUTORIAL', '')
    if len(VERIFY_TUTORIAL) == 0:
        VERIFY_TUTORIAL = 'https://t.me/How_To_Open_Linkl'

    # Shortlink Info
    SHORTLINK_MODE = environ.get('SHORTLINK_MODE', 'False')
    SHORTLINK_MODE = SHORTLINK_MODE.lower() == 'true'

    SHORTLINK_URL = environ.get('SHORTLINK_URL', 'api.shareus.io')
    if len(SHORTLINK_URL) == 0:
        SHORTLINK_URL = ''

    SHORTLINK_API = environ.get('SHORTLINK_API', 'hRPS5vvZc0OGOEUQJMJzPiojoVK2')
    if len(SHORTLINK_API) == 0:
        SHORTLINK_API = ''

    # Others
    MAX_B_TN = environ.get("MAX_B_TN", "5")
    if len(MAX_B_TN) == 0:
        MAX_B_TN = 5

    PORT = environ.get("PORT", "8080")
    if len(PORT) == 0:    
        PORT = 8080

    MSG_ALRT = environ.get('MSG_ALRT', '')
    if len(MSG_ALRT) == 0:    
        MSG_ALRT = 'Hello My Dear Friends ❤️'

    CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
    if len(CUSTOM_FILE_CAPTION) == 0:    
        CUSTOM_FILE_CAPTION = f"{script.CAPTION}"
    else:    
        CUSTOM_FILE_CAPTION = CUSTOM_FILE_CAPTION

    BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", '')
    if len(BATCH_FILE_CAPTION) == 0:    
        BATCH_FILE_CAPTION = f"{script.CAPTION}"
    else:    
        BATCH_FILE_CAPTION = BATCH_FILE_CAPTION

    IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "")
    if len(IMDB_TEMPLATE) == 0:    
        IMDB_TEMPLATE = f"{script.IMDB_TEMPLATE_TXT}"
    else:    
        IMDB_TEMPLATE = IMDB_TEMPLATE

    MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)

    # Online Stream and Download
    STREAM_MODE = environ.get('STREAM_MODE', 'False') # Set True or False
    STREAM_MODE = STREAM_MODE.lower() == 'true'

    MULTI_CLIENT = False

    SLEEP_THRESHOLD = environ.get('SLEEP_THRESHOLD', '60')
    if len(SLEEP_THRESHOLD) == 0:
        SLEEP_THRESHOLD = 60
    else:
        SLEEP_THRESHOLD = int(SLEEP_THRESHOLD)

    PING_INTERVAL = environ.get("PING_INTERVAL", "1200") # 20 minutes
    if len(PING_INTERVAL) == 0:
        PING_INTERVAL = 1200
    else:
        PING_INTERVAL = int(PING_INTERVAL)

    URL = environ.get("URL", "https://redesigned-telegram-j6gjj5xg7x5cp94r-8080.app.github.dev/")
    if len(URL) == 0:
        URL = ''

    RENAME_MODE = environ.get('RENAME_MODE', 'False') # Set True or False
    RENAME_MODE = RENAME_MODE.lower() == 'true'

    AUTO_APPROVE_MODE = environ.get('AUTO_APPROVE_MODE', 'False') # Set True or False
    AUTO_APPROVE_MODE = AUTO_APPROVE_MODE.lower() == 'true'

    config_dict.update({
             "ADMINS": ADMINS,   
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
             'OWNER_ID': OWNER_ID,
             'OWNER_USERNAME': OWNER_USERNAME,
             'PICS': PICS,
             'PING_INTERVAL': PING_INTERVAL,
             'PUBLIC_FILE_CHANNEL': PUBLIC_FILE_CHANNEL,
             'PM_SEARCH': PM_SEARCH,
             'PORT': PORT,
             'P_TTI_SHOW_OFF': P_TTI_SHOW_OFF,
             'PROTECT_CONTENT': PROTECT_CONTENT,
             'PUBLIC_FILE_STORE': PUBLIC_FILE_STORE,
             'PAYMENT_TEXT': PAYMENT_TEXT,
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
             'SUPPORT_CHAT_ID': SUPPORT_CHAT_ID,
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
             'VERIFY_TUTORIAL': VERIFY_TUTORIAL})
    
    if DATABASE_URI:
        await DbManager().update_config(config_dict)

class ButtonMaker:
    def __init__(self):
        self.main_buttons = []
        self.header_buttons = []
        self.footer_buttons = []

    def url(self, text, url, position=None):
        button = InlineKeyboardButton(text=text, url=url)
        if position == "header":
            self.header_buttons.append(button)
        elif position == "footer":
            self.footer_buttons.append(button)
        else:
            self.main_buttons.append(button)

    def callback(self, text, callback_data, position=None):
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        if position == "header":
            self.header_buttons.append(button)
        elif position == "footer":
            self.footer_buttons.append(button)
        else:
            self.main_buttons.append(button)

    def column(self, main_columns=1, header_columns=8, footer_columns=8):
        keyboard = [
            self.main_buttons[i : i + main_columns]
            for i in range(0, len(self.main_buttons), main_columns)
        ]

        if self.header_buttons:
            if len(self.header_buttons) > header_columns:
                header_chunks = [
                    self.header_buttons[i : i + header_columns]
                    for i in range(0, len(self.header_buttons), header_columns)
                ]
                keyboard = header_chunks + keyboard
            else:
                keyboard.insert(0, self.header_buttons)

        if self.footer_buttons:
            if len(self.footer_buttons) > footer_columns:
                footer_chunks = [
                    self.footer_buttons[i : i + footer_columns]
                    for i in range(0, len(self.footer_buttons), footer_columns)
                ]
                keyboard += footer_chunks
            else:
                keyboard.append(self.footer_buttons)

        return InlineKeyboardMarkup(keyboard)


async def get_buttons(key=None, edit_type=None, edit_mode=None, mess=None):
    buttons = ButtonMaker()
    if key is None:
        buttons.callback("Config Variables", "botset var")
        buttons.callback("Close", "botset close")
        msg = "Bot Settings:"
    elif key == "var":
        for k in list(OrderedDict(sorted(config_dict.items())).keys())[
            START : 10 + START
        ]:
            buttons.callback(k, f"botset editvar {k}")
        buttons.callback("Back", "botset back")
        buttons.callback("Close", "botset close")
        for x in range(0, len(config_dict) - 1, 10):
            buttons.callback(
                f"{int(x/10)+1}", f"botset start var {x}", position="footer"
            )
        msg = f"<b>Config Variables<b> | Page: {int(START/10)+1}"
    elif key == "private":
        buttons.callback("Back", "botset back")
        buttons.callback("Close", "botset close")
        msg = "Send private files: config.env, token.pickle, cookies.txt, accounts.zip, terabox.txt, .netrc, or any other files!\n\nTo delete a private file, send only the file name as a text message.\n\n<b>Please note:</b> Changes to .netrc will not take effect for aria2c until it's restarted.\n\n<b>Timeout:</b> 60 seconds"
    elif edit_type == "editvar":
        msg = f"<b>Variable:</b> <code>{key}</code>\n\n"
        msg += f'<b>Description:</b> {bset_display_dict.get(key, "No Description Provided")}\n\n'
        if mess.chat.type == ChatType.PRIVATE:
            msg += f'<b>Value:</b> <code>{config_dict.get(key, "None")}</code>\n\n'
        elif key not in bool_vars:
            buttons.callback(
                "View value", f"botset showvar {key}", position="header"
            )
        buttons.callback("Back", "botset back var", position="footer")
        if key not in bool_vars:
            if not edit_mode:
                buttons.callback("Edit Value", f"botset editvar {key} edit")
            else:
                buttons.callback("Stop Edit", f"botset editvar {key}")
        if (
            key not in ["API_HASH", "API_ID", "OWNER_ID", "BOT_TOKEN"]
            and key not in bool_vars
        ):
            buttons.callback("Reset", f"botset resetvar {key}")
        buttons.callback("Close", "botset close", position="footer")
        if edit_mode and key in [
            "CHANNELS",
            "OWNER_ID",
            "LOG_CHANNEL",
            "API_HASH",
            "API_ID",
            "DATABASE_URI",
            "BOT_TOKEN",
        ]:
            msg += "<b>Note:</b> Restart required for this edit to take effect!\n\n"
        if edit_mode and key not in bool_vars:
            msg += "Send a valid value for the above Var. <b>Timeout:</b> 60 sec"
        if key in bool_vars:
            if not config_dict.get(key):
                buttons.callback("Make it True", f"botset boolvar {key} on")
            else:
                buttons.callback("Make it False", f"botset boolvar {key} off")
    button = buttons.column(1) if key is None else buttons.column(2)
    return msg, button

async def editMessage(message, text, buttons=None, photo=None):
    try:
        if message.media:
            if photo:
                return await message.edit_media(
                    InputMediaPhoto(photo, text), reply_markup=buttons
                )
            return await message.edit_caption(caption=text, reply_markup=buttons)
        await message.edit(
            text=text, disable_web_page_preview=True, reply_markup=buttons
        )
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await editMessage(message, text, buttons, photo)
    except (MessageNotModified, MessageEmpty):
        pass
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)

async def update_buttons(message, key=None, edit_type=None, edit_mode=None):
    msg, button = await get_buttons(key, edit_type, edit_mode, message)
    await editMessage(message, msg, button)

async def edit_variable(_, message, pre_message, key):
    handler_dict[message.chat.id] = False
    value = message.text
    if key == "LOG_CHANNEL":
        value = int(value)
    elif value.isdigit():
        value = int(value)
    config_dict[key] = value
    await update_buttons(pre_message, key, "editvar", False)
    await message.delete()
    if DATABASE_URI:
        await DbManager().update_config({key: value})

async def event_handler(client, query, pfunc, rfunc, document=False):
    chat_id = query.message.chat.id
    handler_dict[chat_id] = True
    start_time = time()

    async def event_filter(_, __, event):
        user = event.from_user or event.sender_chat
        return bool(
            user.id == query.from_user.id
            and event.chat.id == chat_id
            and (event.text or event.document and document)
        )

    handler = client.add_handler(
        MessageHandler(pfunc, filters=create(event_filter)), group=-1
    )
    while handler_dict[chat_id]:
        await sleep(0.5)
        if time() - start_time > 60:
            handler_dict[chat_id] = False
            await rfunc()
    client.remove_handler(*handler)

async def sendFile(message, file, caption=None, buttons=None):
    try:
        return await message.reply_document(
            document=file,
            quote=True,
            caption=caption,
            disable_notification=True,
            reply_markup=buttons,
        )
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendFile(message, file, caption)
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def edit_bot_settings(client, query):
    data = query.data.split()
    message = query.message
    if data[1] == "close":
        handler_dict[message.chat.id] = False
        await query.answer()
        await message.delete()
        await message.reply_to_message.delete()
    elif data[1] == "back":
        handler_dict[message.chat.id] = False
        await query.answer()
        key = data[2] if len(data) == 3 else None
        if key is None:
            globals()["START"] = 0
        await update_buttons(message, key)
    elif data[1] == "var":
        await query.answer()
        await update_buttons(message, data[1])
    elif data[1] == "resetvar":
        handler_dict[message.chat.id] = False
        await query.answer("Reset done!", show_alert=True)
        value = ""
        if data[2] in default_values:
            value = default_values[data[2]]
        config_dict[data[2]] = value
        await update_buttons(message, data[2], "editvar", False)
        if DATABASE_URI:
            await DbManager().update_config({data[2]: value})
    elif data[1] == "boolvar":
        handler_dict[message.chat.id] = False
        value = data[3] == "on"
        await query.answer(
            f"Successfully variable	 changed to {value}!", show_alert=True
        )
        config_dict[data[2]] = value
        await update_buttons(message, data[2], "editvar", False)
        if DATABASE_URI:
            await DbManager().update_config({data[2]: value})
    elif data[1] == "editvar":
        handler_dict[message.chat.id] = False
        await query.answer()
        edit_mode = len(data) == 4
        await update_buttons(message, data[2], data[1], edit_mode)
        if data[2] in bool_vars or not edit_mode:
            return
        pfunc = partial(edit_variable, pre_message=message, key=data[2])
        rfunc = partial(update_buttons, message, data[2], data[1], edit_mode)
        await event_handler(client, query, pfunc, rfunc)
    elif data[1] == "showvar":
        value = config_dict[data[2]]
        if len(str(value)) > 200:
            await query.answer()
            with BytesIO(str.encode(value)) as out_file:
                out_file.name = f"{data[2]}.txt"
                await sendFile(message, out_file)
            return
        if value == "":
            value = None
        await query.answer(f"{value}", show_alert=True)
    elif data[1] == "edit":
        await query.answer()
        globals()["STATE"] = "edit"
        await update_buttons(message, data[2])
    elif data[1] == "view":
        await query.answer()
        globals()["STATE"] = "view"
        await update_buttons(message, data[2])
    elif data[1] == "start":
        await query.answer()
        if int(data[3]) != START:
            globals()["START"] = int(data[3])
            await update_buttons(message, data[2])

async def sendMessage(message, text, buttons=None, photo=None):
    try:
        return await message.reply(
            text=text,
            quote=True,
            disable_web_page_preview=True,
            disable_notification=True,
            reply_markup=buttons,
        )
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(message, text, buttons, photo)
    except ReplyMarkupInvalid:
        return await sendMessage(message, text, None, photo)
    except Exception as e:
        LOGGER.error(format_exc())
        return str(e)

@Client.on_message(filters.command("bs") & filters.user(ADMINS))
async def bot_settings(_, message):
    msg, button = await get_buttons()
    globals()["START"] = 0
    await sendMessage(message, msg, button)

@Client.on_callback_query(filters.regex("^botset"))
async def edit_bot_set_call(client: Client, query: CallbackQuery):
    await edit_bot_settings(client, query)