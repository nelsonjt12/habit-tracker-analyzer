# Habit Tracker Analyzer

A data-driven Python web application that transforms habit tracking data from Google Sheets into actionable insights through interactive visualizations and statistical analysis.

## [View Live Demo](https://habit-tracker-analyzer.onrender.com) | [GitHub Repository](https://github.com/nelsonjt12/habit-tracker-analyzer)

## Project Overview

The Habit Tracker Analyzer is a full-stack application that helps users visualize their habit completion patterns, identify trends, and improve consistency through an intuitive dashboard. By connecting directly to Google Sheets as a data source, it provides real-time updates and analysis without requiring manual data imports.

### Key Features

- **Comprehensive Analytics**: Calculate weekly and overall habit completion rates with detailed breakdowns
- **Streak Analysis**: Track current and historical streaks to visualize momentum
- **Predictability Metrics**: Identify which habits have the most consistent day-to-day patterns
- **Visual Dashboard**: Interactive charts and heatmaps for data exploration
- **Automated Updates**: Data refreshes automatically via scheduled scripts
- **Responsive Design**: Access insights across devices with a mobile-friendly interface

## Technical Implementation

This project demonstrates proficiency in:

### Backend Development
- **Python & Flask**: Server-side application with RESTful API endpoints
- **Google Sheets API Integration**: Real-time data sourcing and authentication
- **Automated Data Processing**: Scheduled scripts for hands-free updates

### Data Analysis
- **Pandas & NumPy**: Advanced data manipulation and statistical analysis
- **Custom Analytics**: Proprietary algorithms for streak detection and habit predictability scoring
- **Data Transformation**: Raw habit entries converted into actionable metrics

### Frontend & Visualization
- **Dynamic Dashboards**: Interactive data exploration using modern web technologies
- **Matplotlib & Seaborn**: Custom visualizations including completion rate charts and heatmaps
- **Responsive Web Design**: Optimized viewing across desktop and mobile devices

## Interesting Insights

The analysis revealed counterintuitive patterns in my habit data: while Walking was my most frequently completed habit overall, it was also my least predictable when analyzing day-to-day consistency. This demonstrates how the application can surface non-obvious patterns that simple tracking alone would miss.

## Development Journey

This project evolved from a simple CSV-based analysis tool into a fully deployed web application. Key development milestones included:

1. Initial data analysis with Python and Pandas using static CSV files
2. Integration with Google Sheets API for dynamic data sourcing
3. Development of a Flask web dashboard with interactive visualizations
4. Deployment to Render with continuous integration

## Getting Started

### Prerequisites
- Python 3.8+
- Google Account with Sheets access
- API credentials for Google Sheets

### Installation

```bash
# Clone the repository
git clone https://github.com/nelsonjt12/habit-tracker-analyzer.git
cd habit-tracker-analyzer

# Install dependencies
pip install -r requirements.txt

# Set up Google Sheets credentials
# Place your habit-tracker-key.json in the scripts/ folder

# Generate dashboard data
python scripts/generate_dashboard.py

# Start the web server
python app.py
```

### Data Format

The application expects your Google Sheets to follow this structure:

| Date       | Habit1   | Habit2   | Habit3   | Notes     |
|------------|----------|----------|----------|-----------|
| 05/01/2025 | Yes      | No       | Yes      | Optional  |
| 05/02/2025 | Yes      | Yes      | Yes      | More      |

## Future Enhancements

- Machine learning to predict habit success probability
- Calendar heatmap visualizations for yearly patterns
- Daily/weekly email reports with personalized insights
- Multiple user support with authentication

## Contact

[Juliann Nelson](mailto:julianntnelson@gmail.com) - [LinkedIn](https://www.linkedin.com/in/juliannnelson/)
