# Habit Tracker Analyzer

A simple Python project that analyzes habit tracking data to help you visualize progress, identify trends, and improve consistency.

## Features

- Calculates weekly and overall habit completion rates
- Identifies most consistent and least consistent habits
- Tracks streaks and gaps
- Generates visualizations (bar charts, line charts, heatmaps)

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib / Seaborn
- Jupyter Notebook

## Folder Structure

habit-tracker-analyzer/
├── data/ # Store CSV habit tracking data
├── notebooks/ # Jupyter notebook for EDA and visualization
├── visuals/ # Output charts and graphs
├── src/ # Reusable Python scripts for analysis


## Sample CSV Format

| Date       | Exercise | Meditate | Journal |
|------------|----------|----------|---------|
| 2025-05-01 | 1        | 0        | 1       |
| 2025-05-02 | 1        | 1        | 1       |

Dates should be in YYYY-MM-DD format. Habits are 1 (completed) or 0 (not completed).

## Getting Started

1. Clone this repository
2. Add your own habit tracking CSV file to `/data/`
3. Run `habit_analysis.ipynb` in the `/notebooks/` folder

## Future Improvements

- Add Google Sheets integration
- Build a Streamlit dashboard
- Add calendar heatmap visualizations


