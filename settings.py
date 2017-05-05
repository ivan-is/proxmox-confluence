
# general
LOG_LEVEL = 'INFO'
LOG_FILE = 'log/info.log'
LOG_TO_STDOUT = False

# proxmox
PROXMOX_HOST = ''
PROXMOX_PORT = ''
PROXMOX_USER = ''
PROXMOX_PASS = ''

# confluence
CONFL_URL = ''
CONFL_HOST = ''
CONFL_PORT = ''
CONFL_USER = ''
CONFL_PASS = ''

PAGEID = ''
# file with number of last version page
PAGEID_FNAME = ''


try:
    from local_settings import *
except ImportError:
    pass

