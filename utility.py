# Contains the content of the files : data_manager.py
# and currency_converter.py
# Those files have been deleted and functions of both are stored here
import decimal
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


















































































import os
from dotenv import load_dotenv

import google.generativeai as genai # Changed to import as genai for consistency
from google.generativeai import upload_file

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


import io

def parse_ocr(ocr_text, image):
    # Convert PIL image to BytesIO
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    buffer.name = "receipt.png"  # still include name

    # Explicitly set MIME type
    my_file = upload_file(buffer, mime_type="image/png")

    # Use genai.GenerativeModel directly, as the API key is now configured globally
    model = genai.GenerativeModel("gemini-2.0-flash") 
    response = model.generate_content(
    contents=[
        my_file,
        "This image is a scanned receipt. The OCR text is:\n" + ocr_text,
        (
            "Extract and return only line items that represent actual products or services purchased — NOT payment details like 'Cash', "
            "'Tendered', 'Total', or 'Change'. Return the result as a JSON list of objects with exactly these 4 fields per item: "
            "date, description, amount, and currency. "
            "If any of these fields is missing for an item, use the following defaults: "
            "date: '2025-01-01', amount: 1, description: 'Null', currency: 'USD'. "
            "Only include actual purchases in the result. Every item must include all four fields."
        )
    ]
)


    return response.text