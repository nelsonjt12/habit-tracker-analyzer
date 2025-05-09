# Habit Tracker Analyzer

A simple Python project that analyzes habit tracking data from Google Sheets to help visualize progress, identify trends, and improve consistency through an interactive web dashboard.

## Features

- Calculates weekly and overall habit completion rates
- Identifies most consistent and least consistent habits
- Tracks streaks and gaps
- Generates visualizations (bar charts, line charts, heatmaps)

## Tech Stack

- Python
- Flask (Web Dashboard)
- Google Sheets API (Data Source)
- Pandas
- NumPy
- Matplotlib / Seaborn

## Folder Structure

habit-tracker-analyzer/
├── output/
│   ├── data/ # Exported data from Google Sheets
│   └── visuals/ # Generated visualizations
├── scripts/ # Scripts for dashboard generation
├── src/ # Core analysis functions
├── templates/ # HTML templates for Flask dashboard
├── notebooks/ # Jupyter notebook for exploratory data analysis

## Data Format

The application expects your Google Sheets to have the following format:

| Date       | Habit1   | Habit2   | Habit3   | Notes     |
|------------|----------|----------|----------|--------|
| 05/01/2025 | Yes      | No       | Yes      | Optional notes |
| 05/02/2025 | Yes      | Yes      | Yes      | More notes |

Dates should be in MM/DD/YYYY format. Habits are tracked as 'Yes' (completed) or 'No' (not completed). The Notes column is optional.

## Getting Started

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Set up Google Sheets:
   - Create a Google Sheets file named "Habit Tracker"
   - Add your habit data following the format above
   - Create a service account and download credentials as `habit-tracker-key.json` in the `scripts/` folder
   - Share your Google Sheet with the service account email
4. Generate the dashboard data: `scripts/run_dashboard.bat` or `python scripts/generate_dashboard.py`
5. Start the web dashboard: `python app.py`
6. Open your browser to http://localhost:5000

## Features Implemented

- Google Sheets integration for data source
- Interactive Flask web dashboard
- Visualizations of habit tracking data
- Advanced metrics (streaks, consistency, predictability)

## Future Improvements

- Add calendar heatmap visualizations
- User authentication for multiple users
- Mobile-responsive enhancements
- Daily/weekly email reports


