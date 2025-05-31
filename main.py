import streamlit as st
from ocr_reader import ocr_reader
from currency_converter import currency_converter

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Custom CSS Styles
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f0f4f8, #dbe9f4);
        color: #000;
        border-right: 1px solid #ccc;
    }
    section[data-testid="stSidebar"] div[role="button"]:hover {
        background-color: #e0f7fa !important;
        color: #00796b !important;
    }
    .feature-card {
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.2s;
        font-size: 1rem;
        color: #333;
        margin-top: 1rem;
    }
    .feature-card:hover {
        transform: scale(1.03);
    }
    .card-green {
        background: #e6f4ea;
        border-left: 6px solid #2ecc71;
    }
    .card-purple {
        background: #f0e9ff;
        border-left: 6px solid #9b59b6;
    }
    .card-pink {
        background: #ffe9e9;
        border-left: 6px solid #e74c3c;
    }
    .emoji {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .cta-button {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.8rem 1.8rem;
        border-radius: 999px;
        background: linear-gradient(to right, #36d1dc, #5b86e5);
        color: white !important;
        text-decoration: none;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
        display: inline-block;
        margin-top: 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 💰 Welcome to the Expense Tracker")
st.markdown("Track your daily, weekly, or monthly expenses with smart insights and colorful charts.")
st.divider()

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card card-green">
            <div class="emoji">💵</div>
            <h4>Multi-currency Support</h4>
            <p>Manage expenses in different currencies.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card card-purple">
            <div class="emoji">📄</div>
            <h4>Receipt Scanning</h4>
            <p>Auto-capture data from your receipts using OCR.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card card-pink">
            <div class="emoji">📊</div>
            <h4>Visual Analytics</h4>
            <p>Interactive charts and spending summaries.</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Sidebar menu for navigation between OCR and Currency Converter
menu = st.sidebar.selectbox("Select Feature", ["Home", "Receipt OCR", "Currency Converter"])

if menu == "Home":
    st.markdown("### 👉 Use the sidebar to get started")

elif menu == "Receipt OCR":
    ocr_reader()

elif menu == "Currency Converter":
    currency_converter()

st.markdown("---")
st.caption("✨ Made with care to make your expenses colorful and clear.")