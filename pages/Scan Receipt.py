import streamlit as st
from PIL import Image
import pytesseract
import os
import pandas as pd
import json
from utility import parse_ocr

st.set_page_config(page_title="Receipt OCR", layout="centered")

st.title("🧾 Upload a Receipt")
st.caption("Use OCR to extract expense data from your receipt image.")

uploaded_file = st.file_uploader("Choose a receipt image", type=["png", "jpg", "jpeg"])
csv_path = "data/expenses.csv"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)

    with st.spinner("Extracting text with OCR..."):
        text = pytesseract.image_to_string(image)
        formatted_ocr = parse_ocr(text, image)

        st.markdown("### 🧪 Debug: Raw `formatted_ocr` Output")
        st.code(repr(formatted_ocr))  # Display the raw result for debugging

        # --- Fix and parse markdown-formatted JSON if needed ---
        if isinstance(formatted_ocr, str):
            formatted_ocr = formatted_ocr.strip()
            if formatted_ocr.startswith("```json"):
                formatted_ocr = formatted_ocr.removeprefix("```json").removesuffix("```").strip()
            elif formatted_ocr.startswith("```"):
                formatted_ocr = formatted_ocr.strip("`").strip()
            try:
                formatted_ocr = json.loads(formatted_ocr)
            except json.JSONDecodeError as e:
                st.error(f"❌ Failed to parse formatted_ocr string as JSON:\n{e}")
                st.stop()

        # --- Validate ---
        error = None
        if not formatted_ocr:
            error = "formatted_ocr is empty or None."
        elif not isinstance(formatted_ocr, list):
            error = f"Expected a list, got {type(formatted_ocr).__name__}."
        elif not all(isinstance(item, dict) for item in formatted_ocr):
            error = "Not all items in formatted_ocr are dictionaries."
        elif not all(set(["date", "description", "amount", "currency"]).issubset(item.keys()) for item in formatted_ocr):
            error = "One or more entries are missing required keys: 'date', 'description', 'amount', 'currency'."

        if error:
            st.error(f"❌ OCR Parsing Error: {error}")
        else:
            # Load existing data
            if os.path.exists(csv_path):
                df_existing = pd.read_csv(csv_path)
            else:
                df_existing = pd.DataFrame(columns=["Date", "Description", "Amount", "Currency"])

            # Save new entries
            new_entries = pd.DataFrame(formatted_ocr)
            new_entries.rename(columns={
                "date": "Date",
                "description": "Description",
                "amount": "Amount",
                "currency": "Currency"
            }, inplace=True)

            combined_df = pd.concat([df_existing, new_entries], ignore_index=True)
            combined_df.to_csv(csv_path, index=False)
            st.success(f"✅ {len(new_entries)} entries added to expenses.csv")

    st.markdown("### 📝 Raw OCR Text")
    st.code(text)
