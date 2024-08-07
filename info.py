# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


import re
from os import environ
from Script import script 
from logging import  error as log_error

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'TechVJBot')
if SESSION == '':
    log_error("SESSION variable is missing! Exiting now")
    exit(1)
API_ID = int(environ.get('API_ID', '24736263'))
if API_ID == '':
    log_error("API_ID variable is missing! Exiting now")
    exit(1)
API_HASH = environ.get('API_HASH', '4d53732917b73a6bb89c3b2f2f7b0902')
if API_HASH == '':
    log_error("API_HASH variable is missing! Exiting now")
    exit(1)
BOT_TOKEN = environ.get('BOT_TOKEN', "5916043658:AAF9atv0ZRxW7HLKo7c-std_cJFAh-UXo6w")
if BOT_TOKEN == '':
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

# Bot settings
CACHE_TIME = environ.get('CACHE_TIME', "")
if CACHE_TIME == '':
    CACHE_TIME = 1800
else:
    CACHE_TIME = int(CACHE_TIME)
PICS = (environ.get('PICS', '')).split() #SAMPLE PIC
if PICS == '':
    PICS = 'https://graph.org/file/81b325f3e45868ee1a1cd.jpg'
NOR_IMG = environ.get("NOR_IMG", "")
if NOR_IMG == '':
    NOR_IMG = 'https://graph.org/file/b69af2db776e4e85d21ec.jpg'
MELCOW_VID = environ.get("MELCOW_VID", "")
if MELCOW_VID == '':
    MELCOW_VID = 'https://t.me/How_To_Open_Linkl'
SPELL_IMG = environ.get("SPELL_IMG", "")
if SPELL_IMG == '':
    SPELL_IMG = 'https://te.legra.ph/file/15c1ad448dfe472a5cbb8.jpg'

# Admins, Channels & Users
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001862601820'))
if LOG_CHANNEL == '':
    log_error("LOG_CHANNEL variable is missing! Exiting now")
    exit(1)
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1228255863').split()]
if len(ADMINS) == 0:
    log_error("ADMINS variable is missing! Exiting now")
    exit(1)
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001878326006 -1001895151847').split()]
if len(CHANNELS) == 0:
    log_error("CHANNELS variable is missing! Exiting now")
    exit(1)
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []


# auth_channel means force subscribe channel.
# if REQUEST_TO_JOIN_MODE is true then force subscribe work like request to join fsub, else if false then work like normal fsub.
REQUEST_TO_JOIN_MODE = bool(environ.get('REQUEST_TO_JOIN_MODE', False)) # Set True Or False
TRY_AGAIN_BTN = bool(environ.get('TRY_AGAIN_BTN', False)) # Set True Or False (This try again button is only for request to join fsub not for normal fsub)
auth_channel = environ.get('AUTH_CHANNEL', '') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
reqst_channel = environ.get('REQST_CHANNEL_ID', '')
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
support_chat_id = environ.get('SUPPORT_CHAT_ID', '')
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
if len(FILE_STORE_CHANNEL) == 0:
    FILE_STORE_CHANNEL = []
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]
if len(DELETE_CHANNELS) == 0:
    DELETE_CHANNELS = []
# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://LazyIron:LazyIron1937@cluster07.lkpgwop.mongodb.net/?retryWrites=true&w=majority")
if DATABASE_URI == '':
    log_error("DATABASE_URI variable is missing! Exiting now")
    exit(1)
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster07")
if DATABASE_NAME == '':
    log_error("DATABASE_NAME variable is missing! Exiting now")
    exit(1)
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Iron_Files')
if COLLECTION_NAME == '':
    log_error("COLLECTION_NAME variable is missing! Exiting now")
    exit(1)

# Premium And Referal Settings
PREMIUM_AND_REFERAL_MODE = bool(environ.get('PREMIUM_AND_REFERAL_MODE', False)) # Set Ture Or False

# If PREMIUM_AND_REFERAL_MODE is True Then Fill Below Variable, If Flase Then No Need To Fill.
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
    PAYMENT_QR = 'https://graph.org/file/55749b0d3eaee3a5b958b.jpg'

PAYMENT_TEXT = environ.get('PAYMENT_TEXT', '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs - \n\n- 30ʀs - 1 ᴡᴇᴇᴋ\n- 50ʀs - 1 ᴍᴏɴᴛʜs\n- 120ʀs - 3 ᴍᴏɴᴛʜs\n- 220ʀs - 6 ᴍᴏɴᴛʜs\n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n✨ ᴜᴘɪ ɪᴅ - <code>jivshn@okaxis</code>\n\nᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>')
if PAYMENT_TEXT == '':
    PAYMENT_TEXT = '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs - \n\n- 30ʀs - 1 ᴡᴇᴇᴋ\n- 50ʀs - 1 ᴍᴏɴᴛʜs\n- 120ʀs - 3 ᴍᴏɴᴛʜs\n- 220ʀs - 6 ᴍᴏɴᴛʜs\n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n✨ ᴜᴘɪ ɪᴅ - <code>jivshn@okaxis</code>\n\nᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>'
OWNER_USERNAME = environ.get('OWNER_USERNAME', '') # owner username without @
if OWNER_USERNAME == '': 
    OWNER_USERNAME = "LazyIron"
# Clone Information : If Clone Mode Is True Then Bot Clone Other Bots.
CLONE_MODE = bool(environ.get('CLONE_MODE', False)) # Set True or False
CLONE_DATABASE_URI = environ.get('CLONE_DATABASE_URI', "") # Necessary If clone mode is true
if CLONE_MODE == True and CLONE_DATABASE_URI == "":
    log_error("CLONE_DATABASE_URI variable is missing! Exiting now")
    exit(1)
if CLONE_DATABASE_URI != "":
    CLONE_MODE = True
PUBLIC_FILE_CHANNEL = environ.get('PUBLIC_FILE_CHANNEL', '') # Public Channel Username Without @ or without https://t.me/ and Bot Is Admin With Full Right.
if PUBLIC_FILE_CHANNEL == '':
    PUBLIC_FILE_CHANNEL = ''
# Links
GRP_LNK = environ.get('GRP_LNK', '')
if GRP_LNK == '':
    GRP_LNK = 'https://t.me/HUB4VF'
CHNL_LNK = environ.get('CHNL_LNK', '')
if CHNL_LNK == '':
    CHNL_LNK = 'https://t.me/HUB4VF'
TUTORIAL = environ.get('TUTORIAL', '')
if TUTORIAL == '':
    TUTORIAL = 'https://t.me/How_To_Open_Linkl'
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '') # Support Chat Link Without https:// or @
if SUPPORT_CHAT == '':
    SUPPORT_CHAT = 'vj_bot_disscussion'
# True Or False
AI_SPELL_CHECK = bool(environ.get('AI_SPELL_CHECK', False))
PM_SEARCH = bool(environ.get('PM_SEARCH', False))
IS_SHORTLINK = bool(environ.get('IS_SHORTLINK', False))
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', False))
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "False")), False)
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "False"), False)
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), False)
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", False))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Token Verification Info :
VERIFY = bool(environ.get('VERIFY', False))
VERIFY_SECOND_SHORTNER = bool(environ.get('VERIFY_SECOND_SHORTNER', False))
VERIFY_SHORTLINK_URL = environ.get('VERIFY_SHORTLINK_URL', '')
if VERIFY == True and VERIFY_SHORTLINK_URL == '':
    log_error("VERIFY_SHORTLINK_URL Variable is missing")
elif VERIFY_SHORTLINK_URL != '' and VERIFY == False:
    VERIFY = True
else:
    VERIFY_SHORTLINK_URL = ''
VERIFY_SHORTLINK_API = environ.get('VERIFY_SHORTLINK_API', '')
if VERIFY == True and VERIFY_SHORTLINK_API == '':
    log_error("VERIFY_SHORTLINK_API Variable is missing")
elif VERIFY_SHORTLINK_API != '' and VERIFY == False:
    VERIFY = True
else:
    VERIFY_SHORTLINK_API = ''
# if verify second shortner is True then fill below url and api
VERIFY_SND_SHORTLINK_URL = environ.get('VERIFY_SND_SHORTLINK_URL', '')
if VERIFY_SECOND_SHORTNER == True and VERIFY_SND_SHORTLINK_URL == '':
    log_error("VERIFY_SND_SHORTLINK_URL Variable is missing")
elif VERIFY_SND_SHORTLINK_URL != '' and VERIFY_SECOND_SHORTNER == False:
    VERIFY_SECOND_SHORTNER = True
else:
    VERIFY_SND_SHORTLINK_URL = ''
VERIFY_SND_SHORTLINK_API = environ.get('VERIFY_SND_SHORTLINK_API', '')
if VERIFY_SECOND_SHORTNER == True and VERIFY_SND_SHORTLINK_API == '':
    log_error("VERIFY_SND_SHORTLINK_API Variable is missing")
elif VERIFY_SND_SHORTLINK_API != '' and VERIFY_SECOND_SHORTNER == False:
    VERIFY_SECOND_SHORTNER = True
else:
    VERIFY_SND_SHORTLINK_API = ''
VERIFY_TUTORIAL = environ.get('VERIFY_TUTORIAL', '')
if VERIFY_TUTORIAL == '':
    VERIFY_TUTORIAL = 'https://t.me/How_To_Open_Linkl'

# Shortlink Info
SHORTLINK_MODE = bool(environ.get('SHORTLINK_MODE', False))
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'api.shareus.io')
if SHORTLINK_MODE == True and SHORTLINK_URL == '':
    log_error("SHORTLINK_URL Variable is missing")
elif SHORTLINK_URL != '' and SHORTLINK_MODE == False:
    SHORTLINK_MODE = True
else:
    SHORTLINK_URL = ''
SHORTLINK_API = environ.get('SHORTLINK_API', 'hRPS5vvZc0OGOEUQJMJzPiojoVK2')
if SHORTLINK_MODE == True and SHORTLINK_API == '':
    log_error("SHORTLINK_URL Variable is missing")
elif SHORTLINK_API != '' and SHORTLINK_MODE == False:
    SHORTLINK_MODE = True
else:
    SHORTLINK_API = ''

# Others
MAX_B_TN = environ.get("MAX_B_TN", "5")
if MAX_B_TN == '':
    MAX_B_TN = 5
PORT = environ.get("PORT", "8080")
if PORT == '':
    PORT = 8080
MSG_ALRT = environ.get('MSG_ALRT', '')
if MSG_ALRT == '':
    MSG_ALRT = 'Hello My Dear Friends ❤️'
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)

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
STREAM_MODE = bool(environ.get('STREAM_MODE', False)) # Set True or False

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://redesigned-telegram-j6gjj5xg7x5cp94r-8080.app.github.dev/")
if URL == '' and STREAM_MODE == True:
    log_error("URL Variable is missing")
elif URL != '' and STREAM_MODE == False:
    STREAM_MODE = True
else:
    URL = ''


# Rename Info : If True Then Bot Rename File Else Not
RENAME_MODE = bool(environ.get('RENAME_MODE', False)) # Set True or False

# Auto Approve Info : If True Then Bot Approve New Upcoming Join Request Else Not
AUTO_APPROVE_MODE = bool(environ.get('AUTO_APPROVE_MODE', False)) # Set True or False

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