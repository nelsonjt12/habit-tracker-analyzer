# Habit Tracker Dashboard Deployment Guide

This guide walks through the process of deploying your Habit Tracker Dashboard to Render.com for use as a portfolio project.

## Prerequisites

1. A GitHub account
2. Your habit-tracker-analyzer repository on GitHub
3. A Render.com account (free tier works fine)

## Deployment Steps

### Step 1: Prepare Your Repository

We've already made the necessary changes to your codebase:

- Added `gunicorn` to requirements.txt
- Created a `Procfile` for Render
- Set up a Python runtime specification
- Modified app.py to handle both development and production environments
- Added demo mode for portfolio viewing

Ensure these files are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push
```

### Step 2: Set Up Render Web Service

1. Log in to [Render.com](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure your web service with the following settings:
   - **Name**: habit-tracker-dashboard (or your preferred name)
   - **Environment**: Python
   - **Region**: Choose the one closest to you
   - **Branch**: main (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Step 3: Configure Environment Variables

For a portfolio project, you can use demo mode to avoid needing Google Sheets credentials:

1. In your Render dashboard, go to the "Environment" tab of your web service
2. Add the following environment variable:
   - **Key**: `DEMO_MODE`
   - **Value**: `true`

If you want to use real Google Sheets data:

1. Under the "Environment" tab, click "Add Secret File"
2. Set the filename as: `scripts/habit-tracker-key.json`
3. Copy the contents of your Google Sheets API credentials file

### Step 4: Deploy Your Application

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Once deployed, you can access it at the URL provided by Render

## Portfolio Presentation Tips

### 1. Add a Portfolio Section to Your README

Update your README to include information for potential employers:

```markdown
## Portfolio Project Information

This project demonstrates my skills in:
- Python and Flask web development
- Data analysis with Pandas
- Data visualization with Matplotlib/Seaborn
- Integration with Google Sheets API
- UX/UI design with responsive web design
```

### 2. Create a Landing Page

Consider adding a landing page that explains the project before viewers see the dashboard itself.

### 3. Add GitHub Links

Include links to your GitHub repository on the dashboard for potential employers to explore the code.

## Troubleshooting

- **Application Error**: Check the Render logs for specific error messages
- **No Data Showing**: Verify environment variables are set correctly 
- **Visualization Issues**: Check permissions on output directories
