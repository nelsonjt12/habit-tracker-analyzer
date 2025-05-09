import os
import glob
import sys
import json
from flask import Flask, render_template, send_from_directory, request
from datetime import datetime

# Configure path for imports - we'll lazy load modules when needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Lazy load expensive imports only when needed
pandas_loaded = False
analyzer_loaded = False

def load_pandas():
    global pandas_loaded, pd
    if not pandas_loaded:
        import pandas as pd
        pandas_loaded = True
    return pd

def load_analyzer():
    global analyzer_loaded, get_detailed_stats
    if not analyzer_loaded:
        from src.analyzer import get_detailed_stats
        analyzer_loaded = True
    return get_detailed_stats

# Check if we're running in demo mode for portfolio display
# (when no Google Sheets credentials are available)
DEMO_MODE = os.environ.get('DEMO_MODE', 'False').lower() == 'true'

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
    
    # Group files by type (remove date from filename to group them)
    visual_types = {}
    for file_path in visual_files:
        base_name = os.path.basename(file_path)
        # Split by date pattern (assumes format like 'habit_completion_2025-05-08.png')
        file_parts = base_name.split('_')
        if len(file_parts) > 1:
            # Get everything before the date to use as type key
            file_type = '_'.join(file_parts[:-1])  # e.g., 'habit_completion'
            # Add to dictionary with creation time as value for sorting
            if file_type not in visual_types:
                visual_types[file_type] = []
            visual_types[file_type].append({
                'path': file_path,
                'name': base_name,
                'time': os.path.getmtime(file_path)
            })
    
    # For each type, only keep the most recent file
    latest_visuals = []
    for file_type, files in visual_types.items():
        # Sort by modification time, newest first
        sorted_files = sorted(files, key=lambda x: x['time'], reverse=True)
        if sorted_files:
            latest_visuals.append(sorted_files[0]['name'])
    
    # Final list of visualization files to display
    visual_files = latest_visuals
    
    # Get the latest data file for summary statistics
    data_files = glob.glob(os.path.join(DATA_DIR, '*.csv'))
    latest_data = None
    latest_date = None
    summary_stats = None
    
    if data_files:
        # Find the most recent data file
        latest_data = max(data_files, key=os.path.getmtime)
        # Get the modification date
        latest_date = datetime.fromtimestamp(os.path.getmtime(latest_data)).strftime('%B %d, %Y')
        # Load data for summary stats - lazy load pandas
        pd = load_pandas()
        df = pd.read_csv(latest_data)
        
        # Basic statistics
        total_habits = len(df.columns) - 1  # Subtract date column
        # Convert YYYY-MM-DD dates to Month Day, Year format
        start_date = datetime.strptime(df['Date'].iloc[0], '%Y-%m-%d').strftime('%B %d, %Y')
        end_date = datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d').strftime('%B %d, %Y')
        date_range = f"{start_date} to {end_date}"
        
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
        
        # Get detailed statistics for advanced metrics - lazy load analyzer
        get_detailed_stats = load_analyzer()
        detailed_stats = get_detailed_stats(df)
        
        summary_stats = {
            'total_habits': total_habits,
            'date_range': date_range,
            'overall_rate': overall_rate,
            'habit_rates': completion_rates,
            'detailed_stats': detailed_stats  # Add detailed stats to the template context
        }
    
    return render_template('index.html', 
                           visual_files=visual_files, 
                           latest_date=latest_date,
                           summary_stats=summary_stats)

@app.route('/visuals/<filename>')
def serve_visual(filename):
    """Serve visualization images"""
    return send_from_directory(VISUALS_DIR, filename)

# Make sure output directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VISUALS_DIR, exist_ok=True)

# Create sample data file for demo mode
def create_demo_data():
    """Creates sample data for portfolio display when no Google Sheets connection is available"""
    # Only create demo data if none exists
    if not os.path.exists(os.path.join(DATA_DIR, 'habit_data_demo.csv')):
        print("Generating demo data for portfolio display")
        # Lazy load pandas
        pd = load_pandas()
        # Sample habit data
        data = {
            'Date': pd.date_range('2025-04-22', '2025-05-08').strftime('%Y-%m-%d').tolist(),
            'Walk': ['Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'No'],
            'Resistance Training': ['No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'No', 'Yes', 'No'],
            'Yoga': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'Yes'],
            'Notes': ['15 walk outside', 'Did 10 counter pushups; 30 min treadmill walk', '', 'Short yoga sequence before bed', 
                      '30 min walk; 10 counter pushups and a few resistance exercises', '', 'Evening 30 min walk on treadmill',
                      'Hour long walk on the treadmill; 10 counter pushups', 'Tried out a new yoga channel on YT and really enjoyed it',
                      '30 min treadmill walk', '', '', '', '45-min walk', 'Outdoor walk to shake off some frustration', 'Full workout', 'Yoga in the morning']
        }
        df = pd.DataFrame(data)
        
        # Save demo data
        demo_file = os.path.join(DATA_DIR, 'habit_data_demo.csv')
        df.to_csv(demo_file, index=False)
        
        # Generate sample visualizations
        try:
            # Import visualization functions only when needed - lazy loading
            import importlib
            analyzer = importlib.import_module('src.analyzer')
            
            # Generate bar chart visualization
            bar_plot_path = os.path.join(VISUALS_DIR, 'habit_completion_demo.png')
            analyzer.plot_completion_rates(df, save_path=bar_plot_path)
            
            # Generate line chart for habit trends
            line_plot_path = os.path.join(VISUALS_DIR, 'habit_trends_demo.png')
            analyzer.plot_habit_trends(df, save_path=line_plot_path)
        except Exception as e:
            print(f"Error generating demo visualizations: {e}")

# Generate demo data if in demo mode
if DEMO_MODE:
    create_demo_data()

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(BASE_DIR, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Determine if running locally or in production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    # Start the Flask application
    app.run(host='0.0.0.0', debug=debug, port=port)
