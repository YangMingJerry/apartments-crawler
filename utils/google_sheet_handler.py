# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/10
# tool      ：PyCharm
# from __future__ import print_function
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
#
# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#
# # The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'
#
# def main():
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#
#     service = build('sheets', 'v4', credentials=creds)
#
#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                 range=SAMPLE_RANGE_NAME).execute()
#     values = result.get('values', [])
#
#     if not values:
#         print('No data found.')
#     else:
#         print('Name, Major:')
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print('%s, %s' % (row[0], row[4]))
#
# if __name__ == '__main__':
#     main()

instructions = '''https://www.maxlist.xyz/2018/09/25/python_googlesheet_crud/'''

import pygsheets
import pandas as pd

from data import google_sheet_key_path



# df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
# ws.set_dataframe(df1, 'A5', copy_index=True, nan='')

class GoogleSheetHandler:
    def __init__(self, url):
        gc = pygsheets.authorize(service_account_file=google_sheet_key_path)
        self.sh = gc.open_by_url(url)
        self.worksheet = self.sh.worksheet_by_title('forAPI')

    def dataframe_factory(self, out):
        return pd.DataFrame(out).T

    def writeback(self, out, purge=False):
        if purge:
            self.purge()
        index_start = self.get_last_index() + 1
        df_out = self.dataframe_factory(out)
        self.worksheet.set_dataframe(df_out, f'A{index_start}', copy_index=True, nan='')

    def get_last_index(self):
        return len(self.worksheet.get_all_records()) + 2

    def purge(self):
        self.worksheet.clear()

def get_all_sheets(sh):
    return sh.worksheets()

if __name__ == '__main__':
    from app.apartments_crawler import Crawler
    c = Crawler()
    out = c.run(location='brooklyn-ny', beds_num=3, price_low=3000, price_high=4500, is_cat=1, is_washer=1)
    gsh = GoogleSheetHandler('https://docs.google.com/spreadsheets/d/14KGHHymCvKqTNizqU5D8eB5DhqmmlToWl7krQJw0jgo/edit#gid=1316632945')
    # gsh.writeback(out, 5, True)
    gsh.get_last_index()