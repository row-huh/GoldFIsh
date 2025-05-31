# implements ocr
import streamlit as st
from PIL import Image
import pytesseract
import io
import re
from datetime import datetime
from utility import parse_ocr

st.set_page_config(page_title="Receipt OCR", layout="wide")

# Unified Dashboard Styling - matching spending_summary.py
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
    
    /* File uploader container - Remove visible styling */
    .upload-container {
        background: transparent;
        padding: 0;
        margin: 1.5rem auto;
        max-width: 600px;
    }
    
    /* Image container */
    .image-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem auto;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        max-width: 700px;
    }
    
    /* Code block container */
    .code-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem auto;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        max-width: 850px;
    }
    
    /* Section headers */
    h3 {
        color: #fff;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Caption styling */
    .stCaption p {
        color: #E2E8F0 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* File uploader styling - Fixed unwanted box */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px);
    }
    
    .stFileUploader label {
        color: #fff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Hide file uploader additional elements that create unwanted boxes */
    .stFileUploader > div > div:last-child {
        display: none !important;
    }
    
    .stFileUploader [data-testid="fileUploaderFileInput"] + div {
        display: none !important;
    }
    
    .stFileUploader small {
        display: none !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        color: #fff;
        text-align: center;
        font-weight: 600;
    }
    
    /* Code block styling */
    .stCodeBlock > div {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stCodeBlock pre {
        color: #E2E8F0 !important;
        font-weight: 500 !important;
    }
    
    /* Image styling */
    .stImage > div {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🧾 Upload a Receipt</h1>', unsafe_allow_html=True)
st.caption("Use OCR to extract expense data from your receipt image.")

# File uploader in styled container
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a receipt image", type=["png", "jpg", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    # Display the uploaded image in styled container
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Perform OCR
    with st.spinner("Extracting text with OCR..."):
        text = pytesseract.image_to_string(image)
        
        # send text to gemini and ask it to boil it down to date, description, amount, currency
        # using llama coz ocr only returns normal text and the possibilities of writing regex's for this situation are endless (trust me, i tried)
        st.markdown('<div class="code-container">', unsafe_allow_html=True)
        st.markdown("### 🤖 Parsed Receipt Data")
        st.code(parse_ocr(text, image))
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="code-container">', unsafe_allow_html=True)
    st.markdown("### 📝 Raw OCR Text")
    st.code(text)
    st.markdown('</div>', unsafe_allow_html=True)