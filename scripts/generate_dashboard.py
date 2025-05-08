# Ensure required packages are installed: gspread, pandas, oauth2client

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Path to your downloaded credentials JSON file
creds_path = 'path/to/your/habit-tracker-key.json'

# Set up Google Sheets access
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Open your spreadsheet and select worksheet
spreadsheet = client.open("Habit Tracker")
worksheet = spreadsheet.sheet1  # or use .worksheet("Sheet1") if you renamed it

# Convert to DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Show result
print(df.head())

