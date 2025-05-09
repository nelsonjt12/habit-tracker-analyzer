import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # Create a custom color palette that matches our UI
    primary_color = "#6366F1"  # Indigo/purple (matches --primary-color)
    secondary_color = "#10B981"  # Teal/green (matches --secondary-color)
    
    # Create a gradient palette from our primary colors
    # The number of colors should match the number of habits
    n_habits = len(rates)
    custom_palette = sns.color_palette([primary_color, secondary_color], n_colors=n_habits)
    
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
