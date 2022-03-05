from googleapiclient.discovery import build
from google.oauth2 import service_account
import os


class GoogleSheetAPI:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.service_account_file = os.getcwd() +'/google_sheet_api/keys.json'
        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def get_rows_in_spreadsheet(self, spreadsheet_id, cell_range):
        result = self.sheet.values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()
        row_list = result['values']
        return row_list

    def create_spreadsheet(self, title):
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = self.service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        spreadsheet_id = spreadsheet.get('spreadsheetId')
        return spreadsheet_id

    def update_spreadsheet(self, spreadsheet_id, rows_list, cell_range, value_input_operation):
        body = {'values': rows_list}
        result = self.service.spreadsheets().values() \
            .update(spreadsheetId=spreadsheet_id, range=cell_range,
                    valueInputOption=value_input_operation, body=body).execute()
        return result


def get_translated_rows(rows_lst):
    count = 1
    header = True
    for row in rows_lst:
        if header:
            header = False
            row.append("Hindi Translated By Google")
        else:
            row.append("=GOOGLETRANSLATE(A" + str(count) + ",\"en\",\"hi\")")
            count += 1
    return rows_lst
