import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.dates import DateFormatter, WeekdayLocator

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def summarize_habits(df):
    habit_columns = df.columns.drop('Date')
    habit_columns = [col for col in habit_columns if col != 'Notes']  # Exclude Notes column
    summary = {}
    for habit in habit_columns:
        # Convert Yes/No to 1/0 before calculating mean
        numeric_values = df[habit].map(lambda x: 1 if str(x).lower() == 'yes' else 0)
        completion_rate = numeric_values.mean()
        summary[habit] = round(completion_rate * 100, 2)
    return summary

def get_detailed_stats(df):
    """
    Calculate detailed statistics including weekly rates, streaks, and consistency metrics.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the habit tracking data
        
    Returns:
    --------
    dict
        Dictionary containing detailed statistics
    """
    # Make a copy and ensure Date is datetime
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Get habit columns (exclude Date and Notes)
    habit_columns = [col for col in df.columns if col not in ['Date', 'Notes']]
    
    # Create binary columns (1 for Yes, 0 for No)
    for habit in habit_columns:
        df[f'{habit}_binary'] = df[habit].map(lambda x: 1 if str(x).lower() == 'yes' else 0)
    
    # Create weekly statistics
    df['Year_Week'] = df['Date'].dt.strftime('%Y-%U')  # Format: Year-WeekNumber
    weekly_stats = {}
    
    # Get complete weeks (weeks with 7 days of data)
    week_counts = df['Year_Week'].value_counts()
    complete_weeks = week_counts[week_counts >= 5].index.tolist()  # Consider weeks with at least 5 days
    
    if complete_weeks:
        weekly_df = df[df['Year_Week'].isin(complete_weeks)].copy()
        
        # Calculate weekly completion rates
        weekly_rates = {}
        for habit in habit_columns:
            rates_by_week = weekly_df.groupby('Year_Week')[f'{habit}_binary'].mean() * 100
            weekly_rates[habit] = {
                'avg_weekly_rate': round(rates_by_week.mean(), 2),
                'best_week': round(rates_by_week.max(), 2),
                'worst_week': round(rates_by_week.min(), 2),
                'last_week_rate': round(rates_by_week.iloc[-1] if not rates_by_week.empty else 0, 2)
            }
        weekly_stats['weekly_rates'] = weekly_rates
    else:
        # Not enough data for weekly stats
        weekly_stats['weekly_rates'] = None
    
    # Calculate streaks (current and historical)
    streak_stats = {}
    for habit in habit_columns:
        # Create helper columns for streak calculation
        df['streak_group'] = (df[f'{habit}_binary'] != df[f'{habit}_binary'].shift(1)).cumsum()
        
        # Find streaks of completed habits (where binary value is 1)
        completed_streaks = df[df[f'{habit}_binary'] == 1].groupby('streak_group').size()
        longest_streak = completed_streaks.max() if not completed_streaks.empty else 0
        
        # Check if currently on a streak
        if df[f'{habit}_binary'].iloc[-1] == 1:
            current_streak = completed_streaks.iloc[-1] if not completed_streaks.empty else 0
        else:
            current_streak = 0
            
        streak_stats[habit] = {
            'current_streak': int(current_streak),
            'longest_streak': int(longest_streak)
        }
    
    # Calculate consistency metrics
    consistency_stats = {}
    
    # Calculate variance for each habit (lower variance = more consistent)
    variances = {}
    for habit in habit_columns:
        variances[habit] = df[f'{habit}_binary'].var()
    
    # Calculate day-to-day consistency (how often the habit status changes)
    day_to_day = {}
    for habit in habit_columns:
        changes = (df[f'{habit}_binary'] != df[f'{habit}_binary'].shift(1)).sum()
        consistency_score = 100 - (changes / len(df) * 100)  # Higher = more consistent
        day_to_day[habit] = round(consistency_score, 2)
    
    # Find most and least consistent habits based on day-to-day consistency scores
    if day_to_day:
        most_consistent = max(day_to_day, key=day_to_day.get)
        least_consistent = min(day_to_day, key=day_to_day.get)
        
        consistency_stats['most_consistent'] = most_consistent
        consistency_stats['least_consistent'] = least_consistent
        consistency_stats['day_to_day'] = day_to_day
    
    # Combine all statistics
    detailed_stats = {
        'weekly': weekly_stats,
        'streaks': streak_stats,
        'consistency': consistency_stats
    }
    
    return detailed_stats

def plot_completion_rates(df, save_path=None):
    habit_columns = df.columns.drop('Date')
    habit_columns = [col for col in habit_columns if col != 'Notes']  # Exclude Notes column
    
    # Calculate rates by converting Yes/No to 1/0
    rates = {}
    for habit in habit_columns:
        numeric_values = df[habit].map(lambda x: 1 if str(x).lower() == 'yes' else 0)
        rates[habit] = numeric_values.mean() * 100
    
    # Modern styling that matches our UI
    # Set style and color palette to match our website design
    sns.set_style("whitegrid")
    
    # Create a custom color palette that matches our UI - same as in plot_habit_trends
    primary_color = "#6366F1"  # Indigo/purple (matches --primary-color)
    secondary_color = "#10B981"  # Teal/green (matches --secondary-color)
    tertiary_color = "#3B82F6"  # Blue that complements the primary color
    
    # Create a fixed color map to ensure consistency across charts
    habit_colors = {
        'Walk': primary_color,
        'Resistance Training': secondary_color,
        'Yoga': tertiary_color
    }
    
    # Map each habit to its assigned color
    custom_palette = [habit_colors.get(habit, primary_color) for habit in rates.keys()]
    
    plt.figure(figsize=(10, 6), facecolor='white')
    ax = plt.axes()
    ax.set_facecolor('#F9FAFB')  # Match background color (--bg-color)
    
    # Plot with our custom styling
    bars = sns.barplot(x=list(rates.keys()), y=list(rates.values()), palette=custom_palette)
    
    # Enhance bars with gradient (if matplotlib version supports it)
    for i, bar in enumerate(bars.patches):
        # Add subtle border
        bar.set_edgecolor('white')
        bar.set_linewidth(1)
    
    # Add data labels on top of bars
    for i, bar in enumerate(bars.patches):
        bars.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height() + 2,
            f'{list(rates.values())[i]:.1f}%',
            ha='center', va='bottom',
            color='#1F2937',  # Match text color (--text-primary)
            fontsize=9,
            fontweight='bold'
        )
    
    # Style the labels to match our UI - title removed as requested
    plt.title("")  # Empty title as it's shown in the section header
    plt.ylabel("Completion (%)", fontsize=12, color='#6B7280')  # Match text color (--text-secondary)
    plt.xlabel("", fontsize=0)  # Remove x-axis label
    
    # Set y-axis limits and add grid only on y-axis
    plt.ylim(0, 105)  # Give a little extra room for the data labels
    plt.grid(axis='y', alpha=0.3)
    
    # Style the axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E5E7EB')
    ax.spines['bottom'].set_color('#E5E7EB')
    
    # Rotate habit names and adjust their color
    plt.xticks(rotation=45, ha='right', color='#6B7280')
    plt.yticks(color='#6B7280')
    
    # Adjust layout to fit all elements
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=120, bbox_inches='tight', transparent=False)
        plt.close()  # Close the figure to avoid displaying it when running as a scheduled task
    else:
        plt.show()

def plot_habit_trends(df, save_path=None):
    """
    Creates a line chart showing total habit completions over time.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the habit tracking data with Date column
    save_path : str, optional
        Path to save the visualization
    """
    # Make a copy to avoid modifying the original dataframe
    df = df.copy()
    
    # Ensure Date is datetime and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Exclude the Notes column
    habit_columns = [col for col in df.columns if col not in ['Date', 'Notes']]
    
    # Convert Yes/No to 1/0 for calculation
    for habit in habit_columns:
        df[f'{habit}_numeric'] = df[habit].map(lambda x: 1 if str(x).lower() == 'yes' else 0)
    
    # Calculate cumulative sums for each habit
    for habit in habit_columns:
        df[f'{habit}_cumsum'] = df[f'{habit}_numeric'].cumsum()
    
    # Modern styling that matches our UI
    sns.set_style("whitegrid")
    
    # Create a custom color palette that matches our UI - same as in plot_completion_rates
    primary_color = "#6366F1"  # Indigo/purple (matches --primary-color)
    secondary_color = "#10B981"  # Teal/green (matches --secondary-color)
    tertiary_color = "#3B82F6"  # Blue that complements the primary color
    
    # Create a fixed color map to ensure consistency across charts
    habit_colors = {
        'Walk': primary_color,
        'Resistance Training': secondary_color,
        'Yoga': tertiary_color
    }
    
    # Map each habit to its assigned color - ensures consistent colors between charts
    custom_palette = [habit_colors.get(habit, primary_color) for habit in habit_columns]
    
    # Set up the plot
    plt.figure(figsize=(10, 6), facecolor='white')
    ax = plt.axes()
    ax.set_facecolor('#F9FAFB')  # Match background color (--bg-color)
    
    # Plot lines for each habit
    for i, habit in enumerate(habit_columns):
        color = custom_palette[i % len(custom_palette)]
        
        # Plot the cumulative sum line with styling
        line = plt.plot(
            df['Date'], 
            df[f'{habit}_cumsum'],
            marker='o',
            markersize=6,
            linewidth=3,
            color=color,
            label=habit
        )[0]
        
        # Add drop shadow to line for depth
        plt.plot(
            df['Date'], 
            df[f'{habit}_cumsum'],
            linewidth=5,
            color=color,
            alpha=0.2  # Transparent for shadow effect
        )
        
        # Add last value annotation
        last_date = df['Date'].iloc[-1]
        last_value = df[f'{habit}_cumsum'].iloc[-1]
        plt.annotate(
            f'{last_value}',
            xy=(last_date, last_value),
            xytext=(5, 0),
            textcoords='offset points',
            color='#1F2937',
            fontweight='bold',
            fontsize=10
        )
    
    # Style the labels - title removed as requested
    plt.title("")  # Empty title as it's shown in the section header
    plt.ylabel("Total Completions", fontsize=12, color='#6B7280')
    plt.xlabel("", fontsize=0)  # Remove x-axis label
    
    # Format the date on x-axis
    date_format = DateFormatter('%b %d')  # Apr 22 format
    ax.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=30, ha='right', color='#6B7280')
    
    # Style the axes and grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E5E7EB')
    ax.spines['bottom'].set_color('#E5E7EB')
    plt.grid(axis='y', alpha=0.3)
    
    # Add legend with custom styling
    legend = plt.legend(
        loc='upper left',
        frameon=True,
        fontsize=10
    )
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_alpha(0.9)
    frame.set_edgecolor('#E5E7EB')
    
    # Adjust layout
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=120, bbox_inches='tight', transparent=False)
        plt.close()
    else:
        plt.show()
