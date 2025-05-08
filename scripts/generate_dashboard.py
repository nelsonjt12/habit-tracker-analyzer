# Habit Tracker Dashboard Generator
# Pulls data from Google Sheets and generates analytics

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import sys

# Add the project root to the path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.analyzer import summarize_habits, plot_completion_rates

# Create output directories if they don't exist
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
data_dir = os.path.join(output_dir, 'data')
visuals_dir = os.path.join(output_dir, 'visuals')

os.makedirs(data_dir, exist_ok=True)
os.makedirs(visuals_dir, exist_ok=True)

# Path to your downloaded credentials JSON file
creds_path = 'scripts/habit-tracker-key.json'

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

# Process the data
if not df.empty:
    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Save data to CSV
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(data_dir, f'habit_data_{today}.csv')
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
    # Generate summary
    summary = summarize_habits(df)
    print("\nHabit Completion Summary:")
    for habit, rate in summary.items():
        print(f"{habit}: {rate}%")
    
    # Generate visualization
    plot_path = os.path.join(visuals_dir, f'habit_completion_{today}.png')
    plot_completion_rates(df, save_path=plot_path)
    print(f"\nVisualization saved to {plot_path}")
    
    # Display the latest data
    print("\nLatest records:")
    print(df.head())
else:
    print("No data found in the spreadsheet.")
