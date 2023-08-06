"""Config for ipgdrive."""

import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from birch import Birch


IPG_CFG = Birch('ipgdrive')


class CfgKey(object):
    EMAIL = 'email'
    USERNAME = 'username'
    SPREADSHEET_NAME = 'spreadsheet_name'
    FREQ_MINUTES = 'freq_minutes'
    SPREADSHEET_KEY = 'spreadsheet_key'


IPG_DIRPATH = os.path.expanduser('~/.config/ipgdrive/')
DRIVE_KEY_FNAME = 'google_drive_service_account_key.json'
DRIVE_KEY_FPATH = os.path.join(IPG_DIRPATH, DRIVE_KEY_FNAME)

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def get_authenticated_gspread():
    """Returns an authenticated gspread instance."""
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        DRIVE_KEY_FPATH, SCOPE)
    return gspread.authorize(credentials)
