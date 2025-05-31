# implements ocr
import streamlit as st
from PIL import Image
import pytesseract
import io
import re
from datetime import datetime
from utility import parse_ocr

st.set_page_config(page_title="Receipt OCR", layout="wide")

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

    /* Dark theme adjustments */
    [data-theme="dark"] {
        --glass-bg-main: rgba(255, 255, 255, 0.08);
        --glass-bg-sidebar: rgba(0, 0, 0, 0.4);
        --text-primary-main: #f8fafc;
        --text-secondary-main: #e2e8f0;
        --success-bg: rgba(34, 197, 94, 0.15);
        --error-bg: rgba(239, 68, 68, 0.15);
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

    /* High contrast title styling */
    h1 {
        font-weight: 800 !important;
        font-size: 3.8rem !important;
        color: #ffffff !important;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 0.8rem !important;
        letter-spacing: -0.02em !important;
        text-align: center !important;
    }

    /* Enhanced glassmorphism file uploader */
    .stFileUploader > div {
        background: var(--glass-bg-main) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        box-shadow: var(--shadow-light) !important;
        max-width: 520px !important;
        margin: 2rem auto !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader > div:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-heavy) !important;
        border-color: rgba(139, 95, 191, 0.5) !important;
        background: rgba(255, 255, 255, 0.2) !important;
    }

    .stFileUploader label {
        color: var(--text-primary-main) !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    }

    /* Floating image container with high contrast */
    .stImage > div {
        background: var(--glass-bg-main) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-heavy) !important;
        margin: 2rem auto !important;
        max-width: 650px !important;
        transition: all 0.3s ease !important;
    }

    .stImage > div:hover {
        transform: scale(1.02);
        box-shadow: 0 25px 50px rgba(45, 27, 105, 0.4) !important;
        border-color: rgba(139, 95, 191, 0.4) !important;
    }

    /* High contrast code blocks */
    .stCodeBlock > div {
        background: var(--glass-bg-main) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 16px !important;
        box-shadow: var(--shadow-light) !important;
        margin: 1.5rem auto !important;
        max-width: 850px !important;
        overflow: hidden !important;
    }

    .stCodeBlock pre {
        background: rgba(0, 0, 0, 0.2) !important;
        color: var(--text-primary-main) !important;
        font-weight: 500 !important;
    }

    /* Enhanced spinner container */
    .stSpinner > div {
        background: var(--glass-bg-main) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid var(--glass-border-main) !important;
        border-radius: 16px !important;
        padding: 2.5rem !important;
        margin: 2rem auto !important;
        box-shadow: var(--shadow-light) !important;
        max-width: 450px !important;
        color: var(--text-primary-main) !important;
    }

    /* High contrast success/error messages */
    .stSuccess > div {
        background: var(--success-bg) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(34, 197, 94, 0.4) !important;
        border-radius: 16px !important;
        padding: 1.4rem 2rem !important;
        margin: 1.5rem auto !important;
        max-width: 650px !important;
        box-shadow: var(--shadow-light) !important;
        color: var(--text-primary-main) !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    .stError > div {
        background: var(--error-bg) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        border-radius: 16px !important;
        padding: 1.4rem 2rem !important;
        margin: 1.5rem auto !important;
        max-width: 650px !important;
        box-shadow: var(--shadow-light) !important;
        color: var(--text-primary-main) !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Center content with enhanced styling */
    .main-content {
        max-width: 950px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
    }

    /* High contrast caption */
    .stCaption p {
        color: var(--text-secondary-main) !important;
        font-size: 1.3rem !important;
        font-weight: 500 !important;
        margin-bottom: 3rem !important;
        text-align: center !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
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

    /* Enhanced floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .stFileUploader > div {
        animation: float 4s ease-in-out infinite;
    }

    /* Additional contrast enhancements */
    .stMarkdown p, .stMarkdown div {
        color: var(--text-primary-main) !important;
    }

    /* Subheading styling */
    h3 {
        color: var(--text-primary-main) !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
        margin-top: 2rem !important;
    }
    </style>
    </style>
""", unsafe_allow_html=True)

# Center the main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.title("🧾 Upload a Receipt")
st.caption("Use OCR to extract expense data from your receipt image.")

uploaded_file = st.file_uploader("Choose a receipt image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)
    
    # Perform OCR
    with st.spinner("Extracting text with OCR..."):
        text = pytesseract.image_to_string(image)
        
        # send text to gemini and ask it to boil it down to date, description, amount, currency
        # using llama coz ocr only returns normal text and the possibilities of writing regex's for this situation are endless (trust me, i tried)
        st.code(parse_ocr(text, image))
        
        
    st.markdown("### 📝 Raw OCR Text")
    st.code(text)

st.markdown('</div>', unsafe_allow_html=True)