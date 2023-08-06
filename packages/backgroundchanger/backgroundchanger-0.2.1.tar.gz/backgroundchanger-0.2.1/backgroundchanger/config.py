from pathlib import Path
from os import path

AUTHOR = 'Connor Ruggles'
EMAIL = 'conruggles@gmail.com'
VERSION = '0.2.1'
URL = 'https://github.com/rugglcon/python-backgroundchanger'
CONFIG_FOLDER = path.join(Path.home(), '.config', 'python-backgroundchanger')
CONFIG_FILE = path.join(CONFIG_FOLDER, 'unsplash_keys.json')
CONFIG_DOWNLOAD_FOLDER = path.join(CONFIG_FOLDER, 'photos')
LOGFILE = path.join(CONFIG_FOLDER, 'backgroundchanger.log')