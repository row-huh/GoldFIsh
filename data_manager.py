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
