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
    tertiary_color = "#F43F5E"  # Rose/pink
    
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
    
    # Style the title and labels to match our UI
    plt.title("Habit Completion Rates", fontsize=16, fontweight='bold', color='#1F2937')
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
    tertiary_color = "#F43F5E"  # Rose/pink
    
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
    
    # Style the title and labels
    plt.title("Cumulative Habit Completions", fontsize=16, fontweight='bold', color='#1F2937')
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
