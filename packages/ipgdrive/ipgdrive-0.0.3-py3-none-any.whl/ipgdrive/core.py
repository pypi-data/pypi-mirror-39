"""Core functionalities for ipemail."""

import os

from crontab import CronTab

from .cfg import (
    IPG_CFG,
    CfgKey,
)


DPATH = os.path.dirname(os.path.abspath(__file__))
JOB_FPATH = os.path.join(DPATH, 'job.py')
JOB_COMMENT_ID = 'ipgdrive'


def setup_job():
    my_cron = CronTab(user=IPG_CFG[CfgKey.USERNAME])
    minutes = IPG_CFG[CfgKey.FREQ_MINUTES]
    ipg_job = None
    for job in my_cron:
        if job.comment == JOB_COMMENT_ID:
            ipg_job = job
    if ipg_job is None:
        ipg_job = my_cron.new(
            command='python {}'.format(JOB_FPATH),
            comment='ipgdrive',
        )
        ipg_job.minute.every(minutes)
        my_cron.write()
        print("New crontab job created for ipgdrive.")
    else:
        print("Exsiting crontab job found for ipgdrive.")
        ipg_job.minute.every(minutes)
        my_cron.write()
        print("crontab job for ipgdrive updated w minutes={}.".format(minutes))
