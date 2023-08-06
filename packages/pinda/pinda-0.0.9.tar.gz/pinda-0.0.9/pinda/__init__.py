import os

PINDA_CONFIGDIR = os.getenv('PINDA_CONFIGDIR', os.path.join(os.getenv('HOME', '/'), '.pinda'))
PINDA_CONFIGFILE = os.path.join(PINDA_CONFIGDIR, 'pinda.yaml')
