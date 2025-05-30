# Contains the content of the files : data_manager.py
# and currency_converter.py
# Those files have been deleted and functions of both are stored here

import pandas as pd
from datetime import datetime



def load_expenses(file_path="data/expenses.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Description", "Amount", "Currency"])



def save_expense(entry_date, description, amount, currency, file_path="data/expenses.csv"):
    df = pd.DataFrame([{
        "Date": pd.to_datetime(entry_date).date(),
        "Description": description,
        "Amount": amount,
        "Currency": currency
    }])
    try:
        existing = pd.read_csv(file_path)
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(file_path, index=False)



def parse_bank_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        df = df[["Date", "Description", "Amount"]]
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
        return df
    except Exception as e:
        print("Error parsing CSV:", e)
        return None


  # Code for generating Pie and Bar charts
  # Code for generating Pie and Bar charts
import matplotlib.pyplot as plt

def generate_pie_chart(df):
    summary = df.groupby("Description")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(summary, labels=summary.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    return fig


def generate_bar_chart(df):
    summary = df.groupby("Description")["Amount"].sum().sort_values()
    fig, ax = plt.subplots()
    summary.plot(kind="barh", ax=ax)
    ax.set_xlabel("Amount")
    ax.set_ylabel("Description")
    ax.set_title("Spending Summary")
    return fig

