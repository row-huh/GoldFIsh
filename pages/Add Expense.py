import streamlit as st
from datetime import date
from utility import save_expense

st.set_page_config(page_title="Add Expense", layout="wide")

# Unified Dashboard Styling - matching purple theme
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
    
    /* Form container - Remove visible styling */
    .form-container {
        background: transparent;
        padding: 0;
        margin: 2rem auto;
        max-width: 650px;
    }
    
    /* Input Styling */
    .stTextInput > div > input, 
    .stNumberInput > div > input, 
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        color: #333 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > input:focus,
    .stNumberInput > div > input:focus,
    .stSelectbox > div > div:focus,
    .stDateInput > div > div > input:focus {
        border: 2px solid #a855f7 !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15) !important;
        outline: none !important;
    }
    
    /* Labels */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stDateInput > label {
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        margin-bottom: 0.8rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Submit Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 15px !important;
        padding: 1rem 2.5rem !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease !important;
        font-size: 1.2rem !important;
        width: 100% !important;
        margin-top: 2rem !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #9333ea 50%, #a855f7 100%) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(124, 58, 237, 0.6) !important;
    }
    
    /* Success message styling */
    .stSuccess > div {
        background: rgba(34, 197, 94, 0.15) !important;
        color: #22c55e !important;
        border: 1px solid #22c55e !important;
        border-radius: 12px !important;
        padding: 1.2rem 1.8rem !important;
        margin-top: 1.5rem !important;
        backdrop-filter: blur(10px) !important;
        font-weight: 600 !important;
        text-align: center !important;
    }
    
    /* Form section styling */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Selectbox dropdown styling */
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
    }
    
    /* Date input styling */
    .stDateInput > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">➕ Add New Expense</h1>', unsafe_allow_html=True)

# Form Section with consistent styling
st.markdown('<div class="form-container">', unsafe_allow_html=True)

with st.form("expense_form", clear_on_submit=True):
    entry_date = st.date_input("📅 Date", value=date.today())
    description = st.text_input("📝 Description")
    amount = st.number_input("💸 Amount", min_value=0.0, step=0.01, format="%.2f")
    currency = st.selectbox("💱 Currency", ["USD", "EUR", "PKR", "INR", "GBP"])
    submitted = st.form_submit_button("➕ Add Expense")
    
    if submitted:
        save_expense(entry_date, description, amount, currency)
        st.success("✅ Expense added successfully!")

st.markdown('</div>', unsafe_allow_html=True)