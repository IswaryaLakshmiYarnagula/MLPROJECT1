import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# Configuration
JSON_CREDENTIALS_FILE = "text1.json"  # Path to your JSON credentials file
GOOGLE_SHEET_ID = "13pxKxKRePbdOtnb4vHB7phZJ3A0JJFyrthxagCJCDlI"  # Your Google Sheet ID
DAILY_ATTENDANCE_FILE = "report1.csv"  # Replace with your CSV file name

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(JSON_CREDENTIALS_FILE, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(GOOGLE_SHEET_ID)
worksheet = sheet.sheet1  # Assuming attendance data is in the first sheet

# Load attendance list from Google Sheets
attendance_data = pd.DataFrame(worksheet.get_all_records())

# Load daily attendance (presenties) from the CSV file
presenties = pd.read_csv(DAILY_ATTENDANCE_FILE)
present_roll_numbers = set(presenties["roll_number"])

# Add a new column for today's date
current_date = datetime.now().strftime("%Y-%m-%d")
if current_date in attendance_data.columns:
    raise ValueError(f"Attendance for {current_date} has already been marked!")

attendance_data[current_date] = attendance_data["roll_number"].apply(
    lambda roll: "Present" if roll in present_roll_numbers else "Absent"
)

# Update Google Sheet with the new attendance data
worksheet.update([attendance_data.columns.values.tolist()] + attendance_data.values.tolist())

print(f"Attendance for {current_date} has been successfully updated.")