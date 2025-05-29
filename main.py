import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💸 Personal Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form"):
    date = st.date_input("Date", value=datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Add Expense")

if submit:
    new_expense = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount
    }
    st.session_state.expenses.append(new_expense)
    st.success("Expense added!")

expense_df = pd.DataFrame(st.session_state.expenses)

if not expense_df.empty:
    st.subheader("📊 Expense Summary")
    st.dataframe(expense_df)

    total = expense_df["Amount"].sum()
    st.metric("Total Spent", f"Rs. {total:.2f}")

    category_summary = expense_df.groupby("Category")["Amount"].sum().reset_index()
    st.bar_chart(category_summary.set_index("Category"))
else:
    st.info("No expenses added yet. Use the form on the left to add some!")
