import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def summarize_habits(df):
    habit_columns = df.columns.drop('Date')
    summary = {}
    for habit in habit_columns:
        completion_rate = df[habit].mean()
        summary[habit] = round(completion_rate * 100, 2)
    return summary

def plot_completion_rates(df, save_path=None):
    habit_columns = df.columns.drop('Date')
    rates = {habit: df[habit].mean() * 100 for habit in habit_columns}
    plt.figure(figsize=(8, 5))
    sns.barplot(x=list(rates.keys()), y=list(rates.values()))
    plt.title("Habit Completion Rates")
    plt.ylabel("Completion (%)")
    if save_path:
        plt.savefig(save_path)
    plt.show()
