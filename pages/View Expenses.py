import streamlit as st
import pandas as pd
from utility import load_expenses

st.set_page_config(page_title="View Expenses", layout="wide")

# Custom styling to match the Spending Summary page
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #4c1d95 0%, #581c87 50%, #6b21a8 100%);
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #2d1b69 0%, #4c1d95 50%, #581c87 100%) !important;
        color: #fff !important;
        font-weight: 600;
        border-right: 2px solid rgba(139, 95, 191, 0.3) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4) !important;
    }

    section[data-testid="stSidebar"] div[role="button"] {
        color: #fff !important;
        background: rgba(0, 0, 0, 0.3) !important;
        margin: 0.5rem 0.8rem;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        font-weight: 600;
    }

    section[data-testid="stSidebar"] div[role="button"]:hover {
        background: linear-gradient(135deg, #6b21a8 0%, #7c3aed 100%) !important;
        color: #fff !important;
        font-weight: 700;
        transform: translateX(6px) scale(1.02);
        box-shadow: 0 4px 15px rgba(107, 33, 168, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        color: #ffffff;
    }

    .info-box {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        color: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
    }

    .dataframe-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        color: #000000;
    }

    .stDataFrame {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📂 View Expenses</h1>', unsafe_allow_html=True)

# Load and filter data
expenses = load_expenses()
expenses = expenses[expenses["Amount"] > 0]  # Filter positive amounts only

if not expenses.empty:
    # Summary boxes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="info-box">🧾<br>Total Transactions<br><span style="font-size:2rem;">{len(expenses)}</span></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="info-box">💰<br>Total Amount<br><span style="font-size:2rem;">${expenses["Amount"].sum():,.2f}</span></div>', unsafe_allow_html=True)

    with col3:
        avg = expenses["Amount"].mean()
        st.markdown(f'<div class="info-box">📊<br>Average Amount<br><span style="font-size:2rem;">${avg:,.2f}</span></div>', unsafe_allow_html=True)

    # Expense table
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(expenses.reset_index(drop=True), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("📭 No data found. Please upload receipts or add expenses.")
