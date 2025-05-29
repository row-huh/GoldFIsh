import streamlit as st
from data_manager import load_expenses

st.set_page_config(page_title="All Expenses", layout="wide")
st.title("📄 All Expenses")

# 💅 Theme and Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }

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

    /* Table scroll bar and font tweak */
    .stDataFrame {
        background: #fff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 📄 Load and display expenses
df = load_expenses()

if df.empty:
    st.warning("⚠️ No expenses found.")
else:
    st.markdown("### 📋 Detailed Table of All Transactions")
    st.dataframe(df, use_container_width=True)
