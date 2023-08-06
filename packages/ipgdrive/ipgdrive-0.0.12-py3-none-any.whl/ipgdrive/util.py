"""Utils for ipgdrive."""

import os
from datetime import datetime

from .cfg import (
    IPG_DIRPATH,
)


LOG_FNAME = 'ipgdrive.log'
LOG_FPATH = os.path.join(IPG_DIRPATH, LOG_FNAME)


def printlog(string):
    print(string)
    with open(LOG_FPATH, 'at+') as logfile:
        line = '{} |  {}\n'.format(datetime.now(), string)
        logfile.write(line)
