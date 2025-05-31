import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

# Enhanced CSS Styling matching your Scan Receipt design
st.markdown("""
    <style>
    /* CSS Variables for theme adaptability */
    :root {
        --main-bg: linear-gradient(135deg, #2d1b69 0%, #11998e 100%);
        --sidebar-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --purple-gradient: linear-gradient(135deg, #8b5fbf 0%, #4c1d95 100%);
        --glass-bg-main: rgba(255, 255, 255, 0.15);
        --glass-bg-sidebar: rgba(0, 0, 0, 0.3);
        --glass-border-main: rgba(255, 255, 255, 0.2);
        --glass-border-sidebar: rgba(139, 95, 191, 0.3);
        --shadow-light: 0 8px 32px rgba(45, 27, 105, 0.3);
        --shadow-heavy: 0 15px 35px rgba(45, 27, 105, 0.4);
        --text-primary-main: #ffffff;
        --text-secondary-main: #e2e8f0;
        --text-primary-sidebar: #e2e8f0;
        --text-secondary-sidebar: #cbd5e0;
        --success-bg: rgba(34, 197, 94, 0.2);
        --error-bg: rgba(239, 68, 68, 0.2);
    }

    /* Main App background - Dark Purple/Teal */
    .stApp {
        background: var(--main-bg);
        background-attachment: fixed;
        color: var(--text-primary-main);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        min-height: 100vh;
        position: relative;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(139, 95, 191, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(76, 29, 149, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(17, 153, 142, 0.2) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }

    /* Sidebar - Dark Grey/Purple */
    section[data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid var(--glass-border-sidebar) !important;
        padding-top: 1rem;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3) !important;
    }

    section[data-testid="stSidebar"] div[role="button"] {
        color: var(--text-primary-sidebar) !important;
        background: var(--glass-bg-sidebar) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid var(--glass-border-sidebar) !important;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.3rem 0.8rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 600;
        font-size: 0.95rem;
    }

    section[data-testid="stSidebar"] div[role="button"]:hover {
        background: var(--purple-gradient) !important;
        color: white !important;
        transform: translateX(6px) scale(1.02);
        box-shadow: var(--shadow-light);
        border-color: rgba(139, 95, 191, 0.6) !important;
    }

    /* Enhanced glassmorphism feature cards as clickable buttons */
    .feature-card {
        background: var(--glass-bg-main) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 20px !important;
        padding: 2.5rem 1.5rem !important;
        box-shadow: var(--shadow-light) !important;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 1rem;
        color: var(--text-primary-main) !important;
        margin: 1.5rem 0.5rem;
        cursor: pointer;
        text-decoration: none;
        display: block;
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }

    .feature-card:hover::before {
        left: 100%;
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: var(--shadow-heavy) !important;
        border-color: rgba(139, 95, 191, 0.5) !important;
        background: rgba(255, 255, 255, 0.2) !important;
    }

    .card-green {
        border-left: 6px solid #2ecc71 !important;
    }
    .card-green:hover {
        border-left: 6px solid #27ae60 !important;
    }

    .card-purple {
        border-left: 6px solid #9b59b6 !important;
    }
    .card-purple:hover {
        border-left: 6px solid #8e44ad !important;
    }

    .card-pink {
        border-left: 6px solid #e74c3c !important;
    }
    .card-pink:hover {
        border-left: 6px solid #c0392b !important;
    }

    .emoji {
        font-size: 3.5rem !important;
        margin-bottom: 1rem !important;
        display: block;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    .feature-card h4 {
        color: var(--text-primary-main) !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        margin-bottom: 0.8rem !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    }

    .feature-card p {
        color: var(--text-secondary-main) !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        text-shadow: 0 1px 8px rgba(0, 0, 0, 0.2) !important;
    }

    /* Enhanced CTA button */
    .cta-button {
        background: var(--accent-gradient) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 50px !important;
        padding: 1.2rem 3rem !important;
        box-shadow: var(--shadow-light) !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: white !important;
        text-decoration: none !important;
        display: inline-block !important;
        margin: 2rem auto !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
        cursor: pointer;
    }

    .cta-button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: var(--shadow-heavy) !important;
        background: var(--purple-gradient) !important;
        border-color: rgba(139, 95, 191, 0.6) !important;
    }

    /* Main title styling */
    h2 {
        font-weight: 800 !important;
        font-size: 3.2rem !important;
        color: #ffffff !important;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 0.8rem !important;
        letter-spacing: -0.02em !important;
        text-align: center !important;
    }

    /* Subtitle styling */
    .subtitle {
        color: var(--text-secondary-main) !important;
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        margin-bottom: 3rem !important;
        text-align: center !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
    }

    /* Divider styling */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--glass-border-main) !important;
        margin: 3rem 0 !important;
        opacity: 0.6 !important;
    }

    /* Footer styling */
    .stCaption p {
        color: var(--text-secondary-main) !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        text-align: center !important;
        text-shadow: 0 1px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    .feature-card:nth-child(1) {
        animation: float 3s ease-in-out infinite;
        animation-delay: 0s;
    }

    .feature-card:nth-child(2) {
        animation: float 3s ease-in-out infinite;
        animation-delay: 1s;
    }

    .feature-card:nth-child(3) {
        animation: float 3s ease-in-out infinite;
        animation-delay: 2s;
    }

    /* Enhanced button styling */
    .stButton > button {
        background: var(--accent-gradient) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        box-shadow: var(--shadow-light) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        margin: 1rem auto !important;
        display: block !important;
        max-width: 300px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: var(--shadow-heavy) !important;
        background: var(--purple-gradient) !important;
        border-color: rgba(139, 95, 191, 0.6) !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--purple-gradient);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #9f7aea 0%, #553c9a 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("## 💰 Welcome to the Expense Tracker")
st.markdown('<p class="subtitle">Track your daily, weekly, or monthly expenses with smart insights and colorful charts.</p>', unsafe_allow_html=True)
st.divider()

# Navigation function
def navigate_to_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# Feature Cards as clickable buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("", key="multi_currency"):
        navigate_to_page("Add Expense")
    st.markdown("""<div class="feature-card card-green" onclick="document.querySelector('[data-testid=\"stButton\"][key=\"multi_currency\"] button').click()">
        <div class="emoji">💵</div>
        <h4>Multi-currency Support</h4>
        <p>Manage expenses in different currencies with real-time conversion rates.</p>
    </div>""", unsafe_allow_html=True)

with col2:
    if st.button("", key="receipt_scan"):
        navigate_to_page("Scan Receipt")
    st.markdown("""<div class="feature-card card-purple" onclick="document.querySelector('[data-testid=\"stButton\"][key=\"receipt_scan\"] button').click()">
        <div class="emoji">📄</div>
        <h4>Receipt Scanning</h4>
        <p>Auto-capture data from your receipts using advanced OCR technology.</p>
    </div>""", unsafe_allow_html=True)

with col3:
    if st.button("", key="visual_analytics"):
        navigate_to_page("Spending Summary")
    st.markdown("""<div class="feature-card card-pink" onclick="document.querySelector('[data-testid=\"stButton\"][key=\"visual_analytics\"] button').click()">
        <div class="emoji">📊</div>
        <h4>Visual Analytics</h4>
        <p>Interactive charts and comprehensive spending summaries.</p>
    </div>""", unsafe_allow_html=True)

st.divider()

# Interactive buttons for quick actions
col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("🚀 Scan Your Receipt Now"):
        navigate_to_page("Scan Receipt")

with col_b:
    if st.button("➕ Add New Expense"):
        navigate_to_page("Add Expense")

with col_c:
    if st.button("📈 View Summary"):
        navigate_to_page("Spending Summary")

# Main CTA
st.markdown("### 👉 Use the sidebar to get started")
if st.button("🎯 Let's Go", key="main_cta"):
    navigate_to_page("Add Expense")

# Footer
st.markdown("---")
st.caption("✨ Made with care to make your expenses colorful and clear.")

# JavaScript to make cards clickable (fallback)
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            const cardClasses = this.classList;
            if (cardClasses.contains('card-green')) {
                // Navigate to Add Expense
                window.parent.postMessage({type: 'navigate', page: 'Add Expense'}, '*');
            } else if (cardClasses.contains('card-purple')) {
                // Navigate to Scan Receipt
                window.parent.postMessage({type: 'navigate', page: 'Scan Receipt'}, '*');
            } else if (cardClasses.contains('card-pink')) {
                // Navigate to Spending Summary
                window.parent.postMessage({type: 'navigate', page: 'Spending Summary'}, '*');
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)