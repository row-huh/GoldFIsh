import streamlit as st

st.markdown("""
<style>
.main-title {
    font-size: 2.8rem;
    font-weight: 900;
    text-align: center;
    color: #d147a3;  /* vibrant pink-purple */
    margin-bottom: 0.8rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-shadow: 1px 1px 3px rgba(209, 71, 163, 0.6);
}
.subtitle {
    text-align: center;
    color: #cba1ce; /* lighter lavender */
    margin-bottom: 2.5rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 500;
    font-size: 1.1rem;
}
.nav-box {
    background: linear-gradient(135deg, #b46aad, #8e4a9e);
    border-radius: 25px;
    padding: 30px 25px;
    text-align: center;
    transition: 0.35s ease;
    color: white;
    height: 220px;
    box-shadow: 0 6px 18px rgba(148, 83, 154, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    user-select: none;
}
.nav-box:hover {
    background: linear-gradient(135deg, #d147a3, #a148a6);
    transform: scale(1.07);
    cursor: pointer;
    box-shadow: 0 10px 28px rgba(209, 71, 163, 0.7);
}
.nav-box-icon {
    font-size: 2.8rem;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 4px rgba(255, 182, 193, 0.7));
}
.nav-box-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    letter-spacing: 0.04em;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.nav-box-desc {
    font-size: 1rem;
    color: #e3c9e8;
    line-height: 1.4;
    font-weight: 400;
}
a {
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💰 Welcome to the Expense Tracker</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track your daily, weekly, or monthly expenses with smart insights and colorful charts.</p>', unsafe_allow_html=True)

# NAVIGATION BOXES SECTION
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <a href="/Add_Expense">
            <div class="nav-box">
                <div class="nav-box-icon">➕</div>
                <div class="nav-box-title">Add New Expense</div>
                <div class="nav-box-desc">Quickly log your daily expenses with multi-currency support and smart categorization.</div>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <a href="/Import_Bank_CSV">
            <div class="nav-box">
                <div class="nav-box-icon">📁</div>
                <div class="nav-box-title">Import Bank CSV</div>
                <div class="nav-box-desc">Upload and parse your bank statements automatically for bulk expense import.</div>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <a href="/Receipt_Scanning">
            <div class="nav-box">
                <div class="nav-box-icon">🧾</div>
                <div class="nav-box-title">Receipt Scanning</div>
                <div class="nav-box-desc">Auto-capture data from your receipts using advanced OCR technology.</div>
            </div>
        </a>
    """, unsafe_allow_html=True)
