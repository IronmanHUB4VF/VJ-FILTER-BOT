#!/usr/bin/env python3
from Script import script
from tzlocal import get_localzone
from pytz import timezone
from datetime import datetime
from inspect import signature
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, enums, utils as pyroutils
from pymongo import MongoClient
from asyncio import Lock
from dotenv import load_dotenv, dotenv_values
from threading import Thread
from time import sleep, time
from subprocess import Popen, run as srun
from os import remove as osremove, path as ospath, environ, getcwd
from socket import setdefaulttimeout
from logging import getLogger, Formatter, FileHandler, StreamHandler, INFO, ERROR, basicConfig, error as log_error, info as log_info, warning as log_warning
import re



load_dotenv('config.env', override=True)

Interval = []
QbInterval = []
QbTorrents = {}
GLOBAL_EXTENSION_FILTER = ['aria2', '!qB']
user_data = {}
extra_buttons = {}
list_drives_dict = {}
shorteners_list = []
categories_dict = {}
aria2_options = {}
qbit_options = {}
queued_dl = {}
queued_up = {}
bot_cache = {}
non_queued_dl = set()
non_queued_up = set()

download_dict_lock = Lock()
status_reply_dict_lock = Lock()
queue_dict_lock = Lock()
qb_listener_lock = Lock()
status_reply_dict = {}
download_dict = {}
rss_dict = {}
id_pattern = re.compile(r'^.\d+$')

BOT_TOKEN = environ.get('BOT_TOKEN', '') #Authentication Token for connect with your Bot
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0] #Dont't touch this

DATABASE_URI = environ.get('DATABASE_URI', '') #Mongodb URI to connect with your MongoDB Database Example:- mongodb+srv://Username:Password@cluster0.lkpgwop.mongodb.net/?retryWrites=true&w=majority
if len(DATABASE_URI) == 0:
    DATABASE_URI = ''

if DATABASE_URI:
    conn = MongoClient(DATABASE_URI)
    db = conn.wzmlx
    current_config = dict(dotenv_values('config.env'))
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    if old_config is None:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    else:
        del old_config['_id']
    if old_config and old_config != current_config:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    elif config_dict := db.settings.config.find_one({'_id': bot_id}):
        del config_dict['_id']
        for key, value in config_dict.items():
            environ[key] = str(value)
    if pf_dict := db.settings.files.find_one({'_id': bot_id}):
        del pf_dict['_id']
        for key, value in pf_dict.items():
            if value:
                file_ = key.replace('__', '.')
                with open(file_, 'wb+') as f:
                    f.write(value)
    conn.close()
    BOT_TOKEN = environ.get('BOT_TOKEN', '')
    bot_id = BOT_TOKEN.split(':', 1)[0]
    DATABASE_URL = environ.get('DATABASE_URI', '')
else:
    config_dict = {}

DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster07")
if DATABASE_NAME == '':
    log_error("DATABASE_NAME variable is missing! Exiting now")
    exit(1)
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Iron_Files')
if COLLECTION_NAME == '':
    log_error("COLLECTION_NAME variable is missing! Exiting now")
    exit(1)

OWNER_ID = environ.get('OWNER_ID', '')
if len(OWNER_ID) == 0:
    log_error("OWNER_ID variable is missing! Exiting now")
    exit(1)
else:
    OWNER_ID = int(OWNER_ID)

ADMINS = environ.get('ADMINS', '')
if len(ADMINS) == 0:
    log_error("OWNER_ID variable is missing! Exiting now")
    exit(1)
else:
    ADMINS = int(ADMINS)

AUTH_USERS = environ.get('AUTH_USERS', '')
if len(AUTH_USERS) != 0:
    aid = AUTH_USERS.split()
    for id_ in aid:
        user_data[int(id_.strip())] = {'is_sudo': True}

AUTH_CHANNEL = environ.get('AUTH_CHANNEL', '')
if len(AUTH_CHANNEL) == 0:
    AUTH_CHANNEL = ''

REQST_CHANNEL = environ.get('REQST_CHANNEL', '')
if len(REQST_CHANNEL) == 0:
    REQST_CHANNEL = ''

API_ID = environ.get('API_ID', '')
if len(API_ID) == 0:
    log_error("API_ID variable is missing! Exiting now")
    exit(1)
else:
    API_ID = int(API_ID)

API_HASH = environ.get('API_HASH', '')
if len(API_HASH) == 0:
    log_error("API_HASH variable is missing! Exiting now")
    exit(1)

LOG_CHANNEL = environ.get('LOG_CHANNEL', '-1001862601820')
if len(LOG_CHANNEL) == 0:
    log_error("LOG_CHANNEL variable is missing! Exiting now")
    exit(1)
else:
    LOG_CHANNEL = int(LOG_CHANNEL)

CHANNELS = environ.get('CHANNELS', '-1001878326006 -1001895151847')
if len(CHANNELS) == 0:
    log_error("CHANNELS variable is missing! Exiting now")
    exit(1)

CACHE_TIME = environ.get('CACHE_TIME', "")
if len(CACHE_TIME) == 0:
    CACHE_TIME = 1800
else:
    CACHE_TIME = int(CACHE_TIME)

CMD_SUFFIX = environ.get("CMD_SUFFIX", "")

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

user = ''
USER_SESSION_STRING = environ.get('USER_SESSION_STRING', '')
if len(USER_SESSION_STRING) != 0:
    log_info("Creating client from USER_SESSION_STRING")
    try:
        user = Client('user', API_ID, API_HASH, session_string=USER_SESSION_STRING,
                        parse_mode=enums.ParseMode.HTML, no_updates=True).start()
    except Exception as e:
        log_error(f"Failed making client from USER_SESSION_STRING : {e}")
        user = ''

# Choose Option Settings 
LANGUAGES = ["malayalam", "mal", "tamil", "tam" ,"english", "eng", "hindi", "hin", "telugu", "tel", "kannada", "kan"]
SEASONS = ["season 1", "season 2", "season 3", "season 4", "season 5", "season 6", "season 7", "season 8", "season 9", "season 10"]
EPISODES = ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29", "E30", "E31", "E32", "E33", "E34", "E35", "E36", "E37", "E38", "E39", "E40"]
QUALITIES = ["360p", "480p", "720p", "1080p", "1440p", "2160p"]
YEARS = ["1900", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]


                           # Don't Remove Credit @VJ_Botz
                           # Subscribe YouTube Channel For Amazing Bot @Tech_VJ
                           # Ask Doubt on telegram @KingVJ01


# Online Stream and Download
STREAM_MODE = environ.get('STREAM_MODE', 'False') # Set True or False
STREAM_MODE = STREAM_MODE.lower() == 'true'

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
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

if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://redesigned-telegram-j6gjj5xg7x5cp94r-8080.app.github.dev/")
if len(URL) == 0:
    URL = ''

# Rename Info : If True Then Bot Rename File Else Not
RENAME_MODE = environ.get('RENAME_MODE', 'False') # Set True or False
RENAME_MODE = RENAME_MODE.lower() == 'true'

# Auto Approve Info : If True Then Bot Approve New Upcoming Join Request Else Not
AUTO_APPROVE_MODE = environ.get('AUTO_APPROVE_MODE', 'False') # Set True or False
AUTO_APPROVE_MODE = AUTO_APPROVE_MODE.lower() == 'true'

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"


# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
config_dict = {
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
             'VERIFY_TUTORIAL': VERIFY_TUTORIAL
}
