import streamlit as st

st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

# Custom CSS for the dashboard
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #4c1d95 0%, #581c87 50%, #6b21a8 100%);
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Hide sidebar by default on main page */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide the invisible buttons completely */
    .stButton > button[key*="_box"] {
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        border: none !important;
        background: none !important;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        color: #ffffff;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        opacity: 0.95;
        color: #e2e8f0;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Navigation box styling */
    .nav-box {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        text-align: center;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .nav-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.05);
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 20px;
    }
    
    .nav-box:hover::before {
        opacity: 1;
    }
    
    .nav-box:hover {
        transform: translateY(-8px) scale(1.02);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .nav-box-icon {
        font-size: 3.5rem;
        margin-bottom: 1.2rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    
    .nav-box-title {
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    .nav-box-desc {
        font-size: 1rem;
        opacity: 0.9;
        line-height: 1.5;
        color: #e2e8f0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Color variants for boxes with darker contrasted borders */
    .box-green {
        border-left: 5px solid #059669;
        background: linear-gradient(135deg, rgba(5, 150, 105, 0.1) 0%, rgba(255, 255, 255, 0.08) 100%);
    }
    
    .box-purple {
        border-left: 5px solid #7c3aed;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(255, 255, 255, 0.08) 100%);
    }
    
    .box-orange {
        border-left: 5px solid #d97706;
        background: linear-gradient(135deg, rgba(217, 119, 6, 0.1) 0%, rgba(255, 255, 255, 0.08) 100%);
    }
    
    .box-blue {
        border-left: 5px solid #2563eb;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(255, 255, 255, 0.08) 100%);
    }
    
    .box-pink {
        border-left: 5px solid #db2777;
        background: linear-gradient(135deg, rgba(219, 39, 119, 0.1) 0%, rgba(255, 255, 255, 0.08) 100%);
    }
    
    /* Action buttons */
    .stButton > button {
        background: linear-gradient(45deg, #7c3aed, #a855f7) !important;
        color: white !important;
        padding: 0.8rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin: 0.5rem auto !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        width: 100% !important;
        max-width: 250px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.6) !important;
        background: linear-gradient(45deg, #8b5cf6, #c084fc) !important;
    }
    
    /* Bottom section */
    .bottom-section {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .bottom-section h3 {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    .footer-text {
        opacity: 0.8;
        font-size: 1rem;
        color: #e2e8f0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-top: 2rem;
    }
    
    /* Make entire columns clickable */
    .stColumn {
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Content
st.markdown('<h1 class="main-title">💰 Welcome to the Expense Tracker</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track your daily, weekly, or monthly expenses with smart insights and colorful charts.</p>', unsafe_allow_html=True)

# Navigation Boxes
col1, col2, col3 = st.columns(3)

with col1:
    # Hidden button for navigation
    if st.button("", key="add_expense_box", help="Add New Expense"):
        st.switch_page("pages/Add Expense.py")
    
    # Clickable box that triggers the hidden button
    st.markdown("""
        <div class="nav-box box-green" onclick="document.querySelector('[data-testid=\\"stButton\\"] button[title=\\"Add New Expense\\"]').click()">
            <div class="nav-box-icon">➕</div>
            <div class="nav-box-title">Add New Expense</div>
            <div class="nav-box-desc">Quickly log your daily expenses with multi-currency support and smart categorization.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("", key="import_csv_box", help="Import Bank CSV"):
        st.switch_page("pages/Import CSV.py")
    
    st.markdown("""
        <div class="nav-box box-purple" onclick="document.querySelector('[data-testid=\\"stButton\\"] button[title=\\"Import Bank CSV\\"]').click()">
            <div class="nav-box-icon">📂</div>
            <div class="nav-box-title">Import Bank CSV</div>
            <div class="nav-box-desc">Upload and parse your bank statements automatically for bulk expense import.</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("", key="scan_receipt_box", help="Scan Receipt"):
        st.switch_page("pages/Scan Receipt.py")
    
    st.markdown("""
        <div class="nav-box box-orange" onclick="document.querySelector('[data-testid=\\"stButton\\"] button[title=\\"Scan Receipt\\"]').click()">
            <div class="nav-box-icon">📱</div>
            <div class="nav-box-title">Receipt Scanning</div>
            <div class="nav-box-desc">Auto-capture data from your receipts using advanced OCR technology.</div>
        </div>
    """, unsafe_allow_html=True)

# Second row
col4, col5 = st.columns(2)

with col4:
    if st.button("", key="summary_box", help="Spending Summary"):
        st.switch_page("pages/Spending Summary.py")
    
    st.markdown("""
        <div class="nav-box box-blue" onclick="document.querySelector('[data-testid=\\"stButton\\"] button[title=\\"Spending Summary\\"]').click()">
            <div class="nav-box-icon">📊</div>
            <div class="nav-box-title">Visual Analytics</div>
            <div class="nav-box-desc">Interactive charts and comprehensive spending summaries with beautiful visualizations.</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    if st.button("", key="view_expenses_box", help="View All Expenses"):
        st.switch_page("pages/View Expenses.py")
    
    st.markdown("""
        <div class="nav-box box-pink" onclick="document.querySelector('[data-testid=\\"stButton\\"] button[title=\\"View All Expenses\\"]').click()">
            <div class="nav-box-icon">📄</div>
            <div class="nav-box-title">All Transactions</div>
            <div class="nav-box-desc">Browse, search, and manage all your recorded expenses in one organized table.</div>
        </div>
    """, unsafe_allow_html=True)

# Quick Actions Section
st.markdown('<div class="bottom-section">', unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📸 Scan Your Receipt Now", key="quick_scan"):
        st.switch_page("pages/Scan Receipt.py")

with action_col2:
    if st.button("💸 Add New Expense", key="quick_add"):
        st.switch_page("pages/Add Expense.py")

with action_col3:
    if st.button("📈 View Summary", key="quick_summary"):
        st.switch_page("pages/Spending Summary.py")

st.markdown('<p class="footer-text">💡 Made with care to make your expenses colorful and clear.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# JavaScript to make boxes clickable
st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Add click handlers to nav boxes
        const boxes = document.querySelectorAll('.nav-box');
        boxes.forEach(box => {
            box.addEventListener('click', function() {
                const onclick = this.getAttribute('onclick');
                if (onclick) {
                    try {
                        eval(onclick);
                    } catch(e) {
                        console.log('Navigation click handled');
                    }
                }
            });
        });
    });
    </script>
""", unsafe_allow_html=True)