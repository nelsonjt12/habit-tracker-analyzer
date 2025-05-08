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
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(rates.keys()), y=list(rates.values()))
    plt.title("Habit Completion Rates")
    plt.ylabel("Completion (%)")
    plt.ylim(0, 100)  # Set y-axis to 0-100%
    plt.xticks(rotation=45)  # Rotate habit names for better readability
    plt.tight_layout()  # Adjust layout to fit all elements
    
    if save_path:
        plt.savefig(save_path)
        plt.close()  # Close the figure to avoid displaying it when running as a scheduled task
    else:
        plt.show()
