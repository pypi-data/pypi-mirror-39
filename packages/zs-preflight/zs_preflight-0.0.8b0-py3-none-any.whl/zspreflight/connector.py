import os
import subprocess
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def google_sheets(input_dict):
    if('customer_name' not in input_dict):
        input_dict['customer_name'] = 'no customer name'
    if('host_name' not in input_dict):
        input_dict['host_name'] = 'no host name'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                './ZerostackPreflightCheck-9d8fd4741552.json',
                ['https://spreadsheets.google.com/feeds'])
    client = gspread.authorize(credentials)
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1LYRm6qk5vxtcMdZUBelayu4jsGICqblzoyScXA3PAvk/edit#gid=0')
    worksheet = sheet.add_worksheet(title="%s"%input_dict['host_name'], rows="100", cols="20")
    
    #new_sheet = client.create('%s')%input_dict['customer_name']
    #new_sheet.share('jonathan@zerostack.com', perm_type='user', role='writer')
    #worksheet = new_sheet.add_worksheet(title="%s"%input_dict['host_name'])

class email():
    pass

class google_drive():
    pass

"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credentials = ServiceAccountCredentials.from_json_keyfile_name(
                '/home/builder/ZerostackPreflightCheck-9d8fd4741552.json',
                ['https://spreadsheets.google.com/feeds'])
client = gspread.authorize(credentials)

sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1LYRm6qk5vxtcMdZUBelayu4jsGICqblzoyScXA3PAvk/edit#gid=0')
worksheet = sheet.get_worksheet(0)
all_rows = worksheet.get_all_records()
print all_rows
print len(all_rows)
worksheet.update_acell('A4', 'Bingo!')

worksheet = sheet.get_worksheet(0)
all_rows = worksheet.get_all_records()
print all_rows
print len(all_rows)
cell = worksheet.find("Bingo!")
value = cell.value
row_number = cell.row
column_number = cell.col
print value
print row_number
print column_number
"""