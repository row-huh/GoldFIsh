import streamlit as st
from PIL import Image
import pytesseract
import os
import pandas as pd
import json
from utility import parse_ocr

# Set page config
st.set_page_config(page_title="Receipt OCR", layout="centered")

# Inject CSS styling
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
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        color: #ffffff;
    }
    .upload-container {
        background: transparent;
        padding: 0;
        margin: 1.5rem auto;
        max-width: 600px;
    }
    .image-container, .code-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem auto;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    .image-container {
        max-width: 700px;
    }
    .code-container {
        max-width: 850px;
    }
    h3 {
        color: #fff;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .stCaption p {
        color: #E2E8F0 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
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
    .stFileUploader > div > div:last-child,
    .stFileUploader [data-testid="fileUploaderFileInput"] + div,
    .stFileUploader small {
        display: none !important;
    }
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
    .stImage > div {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main app UI
st.title("📟 Upload a Receipt")
st.caption("Use OCR to extract expense data from your receipt image.")

uploaded_file = st.file_uploader("Choose a receipt image", type=["png", "jpg", "jpeg"])
csv_path = "data/expenses.csv"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)

    with st.spinner("Extracting text with OCR..."):
        text = pytesseract.image_to_string(image)
        formatted_ocr = parse_ocr(text, image)

        if isinstance(formatted_ocr, str):
            formatted_ocr = formatted_ocr.strip()
            if formatted_ocr.startswith("```json"):
                formatted_ocr = formatted_ocr.removeprefix("```json").removesuffix("```").strip()
            elif formatted_ocr.startswith("```"):
                formatted_ocr = formatted_ocr.strip("`").strip()
            try:
                formatted_ocr = json.loads(formatted_ocr)
            except json.JSONDecodeError:
                st.error("❌ Failed to read expense data from receipt.")
                st.stop()

        if (
            not formatted_ocr or
            not isinstance(formatted_ocr, list) or
            not all(isinstance(item, dict) for item in formatted_ocr) or
            not all(set(["date", "description", "amount", "currency"]).issubset(item.keys()) for item in formatted_ocr)
        ):
            st.error("❌ Could not extract valid expense data from the receipt.")
        else:
            if os.path.exists(csv_path):
                df_existing = pd.read_csv(csv_path)
            else:
                df_existing = pd.DataFrame(columns=["Date", "Description", "Amount", "Currency"])

            new_entries = pd.DataFrame(formatted_ocr)
            new_entries.rename(columns={
                "date": "Date",
                "description": "Description",
                "amount": "Amount",
                "currency": "Currency"
            }, inplace=True)

            combined_df = pd.concat([df_existing, new_entries], ignore_index=True)
            combined_df.to_csv(csv_path, index=False)

            st.success("✅ Expense added successfully.")
