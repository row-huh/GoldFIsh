import streamlit as st
from datetime import date
from utility import save_expense

st.set_page_config(page_title="Add Expense", layout="wide")
st.title("➕ Add New Expense")

# Stylish Light Theme with Colorful Touches
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f0f4f8, #dbe9f4);
        color: #2c3e50 !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] .css-1v0mbdj {
        color: #2c3e50 !important;
    }

    section[data-testid="stSidebar"] div[role="button"] {
        color: #2c3e50 !important;
    }

    section[data-testid="stSidebar"] div[role="button"]:hover {
        background-color: #d0f0fd !important;
        color: #0077b6 !important;
        font-weight: 700;
        border-radius: 8px;
    }

    /* Input Styling */
    .stTextInput > div > input, .stNumberInput > div > input, .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #ccc !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }

    /* Submit Button */
    button[kind="primary"] {
        background: linear-gradient(to right, #36d1dc, #5b86e5);
        color: white;
        font-weight: bold;
        border-radius: 999px;
        padding: 0.6rem 1.5rem;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.2s ease-in-out;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(to right, #1fa2ff, #5b86e5);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# Form Section
with st.form("expense_form", clear_on_submit=True):
    entry_date = st.date_input("📅 Date", value=date.today())
    description = st.text_input("📝 Description")
    amount = st.number_input("💸 Amount", min_value=0.0, step=0.01, format="%.2f")
    currency = st.selectbox("💱 Currency", ["USD", "EUR", "PKR", "INR", "GBP"])
    submitted = st.form_submit_button("➕ Add Expense")
    if submitted:
        save_expense(entry_date, description, amount, currency)
        st.success("✅ Expense added successfully!")
