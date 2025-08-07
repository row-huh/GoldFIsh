import streamlit as st

st.markdown("""
<style>
.stApp {
        background: linear-gradient(135deg, #4c1d95 0%, #581c87 50%, #6b21a8 100%);
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }            
.nav-box {
    background: linear-gradient(145deg, #5b21b6, #7e22ce);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    color: #ffffff;
    height: 260px;
    box-shadow: 0 12px 30px rgba(124, 58, 237, 0.25), 0 6px 15px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(6px);
    overflow: hidden;
}

.nav-box:hover {
    transform: translateY(-6px) scale(1.03);
    background: linear-gradient(145deg, #6b21a8, #9333ea);
    box-shadow: 0 18px 40px rgba(168, 85, 247, 0.35), 0 8px 18px rgba(0, 0, 0, 0.3);
    cursor: pointer;
}

/* Link Styling */
a {
    text-decoration: none !important;
    color: inherit !important;
    display: block;
    width: 100%;
    height: 100%;
}
a:hover, a:focus, a:active {
    text-decoration: none !important;
    color: inherit !important;
}

/* Icon */
.nav-box-icon {
    font-size: 2.6rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 6px rgba(255, 255, 255, 0.3));
}

/* Title */
.nav-box-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.7rem;
    letter-spacing: 0.5px;
}

/* Description */
.nav-box-desc {
    font-size: 1rem;
    color: #e9d5ff;
    line-height: 1.4;
    font-weight: 400;
    overflow-wrap: break-word;
    word-break: break-word;
    max-width: 100%;
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
            </div>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <a href="/Import_Bank_CSV">
            <div class="nav-box">
                <div class="nav-box-icon">📁</div>
                <div class="nav-box-title">Import Bank CSV</div>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <a href="/Receipt_Scanning">
            <div class="nav-box">
                <div class="nav-box-icon">🧾</div>
                <div class="nav-box-title">Receipt Scanning</div>
            </div>
        </a>
    """, unsafe_allow_html=True)
