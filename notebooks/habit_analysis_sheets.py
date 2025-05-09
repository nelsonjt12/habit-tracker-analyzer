# Habit Tracker Analyzer (Google Sheets Version)
# This script loads and analyzes habit data directly from Google Sheets

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Set up visual style
sns.set(style='whitegrid')

# Function to load data from Google Sheets
def load_from_google_sheets(creds_path='../scripts/habit-tracker-key.json'):
    """
    Load habit tracking data directly from Google Sheets
    
    Parameters:
    -----------
    creds_path : str
        Path to the Google Sheets API credentials JSON file
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the habit tracking data
    """
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
        
        print(f"Successfully loaded data with {len(df)} records from Google Sheets")
        return df
    else:
        print("No data found in the spreadsheet.")
        return None

# Load the habit tracking data from Google Sheets
try:
    df = load_from_google_sheets()
    
    # Display the first few rows of the data
    print("\nFirst few records:")
    print(df.head())
    
    # Basic summary: calculate completion rates for each habit
    habit_cols = df.columns.drop(['Date', 'Notes'])  # Exclude 'Notes' column
    completion_rates = df[habit_cols].map(lambda x: 1 if x == 'Yes' else 0).mean() * 100  # Convert 'Yes'/'No' to 1/0
    
    # Show completion rates
    print("\nHabit Completion Rates (%):")
    print(completion_rates.round(2))
    
    # Plot habit completion rates
    plt.figure(figsize=(10,5))
    sns.barplot(x=completion_rates.index, y=completion_rates.values)
    plt.title('Habit Completion Rates (%)')
    plt.ylabel('Completion %')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save visualization
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'visuals')
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    plot_path = os.path.join(output_dir, f'habit_completion_{today}.png')
    plt.savefig(plot_path)
    print(f"\nVisualization saved to {plot_path}")
    
    # Show the plot
    plt.show()
    
    # Additional analysis based on the original notebook
    # You can add more analysis as needed
    
except Exception as e:
    print(f"Error: {e}\n")
    print("If you're seeing credential errors, make sure the 'habit-tracker-key.json' file is in the scripts directory")
    print("If you're seeing file not found errors, please check the path to the credentials file")
