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
