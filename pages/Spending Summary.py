import streamlit as st
from utility import load_expenses
from utility import generate_pie_chart, generate_bar_chart  # assuming you saved them in charts.py

st.set_page_config(page_title="Spending Summary", layout="wide")

# Unified Dashboard Styling - matching scan_receipt.py
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #4c1d95 0%, #581c87 50%, #6b21a8 100%);
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Sidebar Styling - Darker purple */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #2d1b69 0%, #4c1d95 50%, #581c87 100%) !important;
        color: #fff !important;
        font-weight: 600;
        border-right: 2px solid rgba(139, 95, 191, 0.3) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    section[data-testid="stSidebar"] .css-1v0mbdj {
        color: #fff !important;
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
    
    /* Main title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        color: #ffffff;
    }
    
    /* Chart containers - Removed glass effect */
    .chart-container {
        background: transparent;
        padding: 1rem;
        margin: 1rem;
    }
    
    /* Section headers */
    h3 {
        color: #fff;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Info message styling */
    .stInfo > div {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 2rem 2.5rem !important;
        margin: 2rem auto !important;
        max-width: 600px !important;
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Matplotlib figure styling */
    .stPlotlyChart,
    .stPyplot {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Column styling for better spacing */
    .stColumn {
        padding: 0 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📊 Spending Summary</h1>', unsafe_allow_html=True)

# Load Data
expenses = load_expenses()
expenses = expenses[expenses["Amount"] > 0]  # Filter positive amounts only

if not expenses.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🥧 Pie Chart")
        pie_fig = generate_pie_chart(expenses)
        st.pyplot(pie_fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Bar Chart")
        bar_fig = generate_bar_chart(expenses)
        st.pyplot(bar_fig)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📭 No data to display. Please add some expenses.")