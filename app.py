import os
import glob
import pandas as pd
from flask import Flask, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__)

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')
VISUALS_DIR = os.path.join(OUTPUT_DIR, 'visuals')

@app.route('/')
def index():
    """Main page that displays habit tracking dashboard"""
    # Get list of available visualizations
    visual_files = glob.glob(os.path.join(VISUALS_DIR, '*.png'))
    visual_files = [os.path.basename(f) for f in visual_files]
    
    # Get the latest data file for summary statistics
    data_files = glob.glob(os.path.join(DATA_DIR, '*.csv'))
    latest_data = None
    latest_date = None
    summary_stats = None
    
    if data_files:
        # Find the most recent data file
        latest_data = max(data_files, key=os.path.getmtime)
        # Get the modification date
        latest_date = datetime.fromtimestamp(os.path.getmtime(latest_data)).strftime('%Y-%m-%d')
        # Load data for summary stats
        df = pd.read_csv(latest_data)
        
        # Basic statistics
        total_habits = len(df.columns) - 1  # Subtract date column
        date_range = f"{df['Date'].iloc[0]} to {df['Date'].iloc[-1]}"
        
        # Calculate overall completion rate
        habit_columns = df.columns.drop('Date')
        completion_rates = {}
        for habit in habit_columns:
            # Convert Yes/No to 1/0 for calculation
            numeric_values = df[habit].map(lambda x: 1 if str(x).lower() == 'yes' else 0)
            completion_rates[habit] = round(numeric_values.mean() * 100, 2)
        
        # Remove the 'Notes' habit if it exists
        if 'Notes' in completion_rates:
            del completion_rates['Notes']
        
        overall_rate = round(sum(completion_rates.values()) / len(completion_rates) if completion_rates else 0, 2)
        
        summary_stats = {
            'total_habits': total_habits,
            'date_range': date_range,
            'overall_rate': overall_rate,
            'habit_rates': completion_rates
        }
    
    return render_template('index.html', 
                           visual_files=visual_files, 
                           latest_date=latest_date,
                           summary_stats=summary_stats)

@app.route('/visuals/<filename>')
def serve_visual(filename):
    """Serve visualization images"""
    return send_from_directory(VISUALS_DIR, filename)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(BASE_DIR, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Start the Flask application
    app.run(debug=True, port=5000)
