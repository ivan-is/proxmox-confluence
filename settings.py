
# general
LOG_LEVEL = 'INFO'
LOG_FILE = 'log/info.log'
LOG_TO_STDOUT = False

# proxmox
PROXMOX_HOST = ''
PROXMOX_PORT = ''
PROXMOX_USER = ''
PROXMOX_PASS = ''

# page settings
PAGEID = ''
PAGE_TITLE = ''

# confluence
CONFL_HOST = ''
CONFL_PORT = ''
CONFL_USER = ''
CONFL_PASS = ''
CONFL_URL = 'http://{host}:{port}/rest/api/content/{page_id}'.format(host=CONFL_HOST,
                                                                     port=CONFL_PORT,
                                                                     page_id=PAGEID)


try:
    from local_settings import *
except ImportError:
    pass

