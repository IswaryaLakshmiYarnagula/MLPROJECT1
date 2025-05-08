import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_FILE = "text1.json"

# Authenticate and connect to Google Sheets
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Google Sheet details
SHEET_ID = "13pxKxKRePbdOtnb4vHB7phZJ3A0JJFyrthxagCJCDlI"
WORKSHEET_NAME = "Attendance_list"

def read_google_sheet():
    sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_google_sheet(df):
    sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

def mark_attendance(attendance_csv):
    df_sheet = read_google_sheet()
    df_presenties = pd.read_csv("cleaned_roll_numbers.csv", header=None, names=['roll_number'])
    present_rolls = set(df_presenties['roll_number'].astype(str))
    
    today = datetime.today().strftime('%Y-%m-%d')
    df_sheet[today] = df_sheet['roll_number'].astype(str).apply(lambda x: "Present" if x in present_rolls else "Absent")
    
    update_google_sheet(df_sheet)
    print("Attendance updated successfully!")

# Run the script with the daily attendance CSV
attendance_file = "cleaned_roll_numbers.csv"
mark_attendance(attendance_file)