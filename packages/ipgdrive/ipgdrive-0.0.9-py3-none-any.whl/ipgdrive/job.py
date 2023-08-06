"""The job to run."""

from datetime import datetime

from requests import get

from .cfg import (
    IPG_CFG,
    CfgKey,
    get_authenticated_gspread,
)


def job_func():
    gc = get_authenticated_gspread()
    ip = get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))
    # sh_name = IPG_CFG[CfgKey.SPREADSHEET_NAME]
    # print('Trying to open spreadsheet {}'.format(sh_name))
    sh_key = IPG_CFG[CfgKey.SPREADSHEET_KEY]
    print('Trying to open spreadsheet with key: {}'.format(sh_key))
    # sh = gc.open(sh_name)
    sh = gc.open_by_key(sh_key)
    # sh = gc.create(ip)
    # email = IPG_CFG[CfgKey.EMAIL]
    # sh.share(email, perm_type='user', role='writer')
    worksheet = sh.get_worksheet(0)
    worksheet.update_acell('A1', 'Ubuntu public ip')
    worksheet.update_acell('A2', ip)
    worksheet.update_acell('B1', 'Last Time Ran')
    worksheet.update_acell('B2', str(datetime.now()))


if __name__ == "__main__":
    job_func()
