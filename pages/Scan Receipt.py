# implements ocr

import streamlit as st
from PIL import Image
import pytesseract
import io
import re
from datetime import datetime
# the actual function is in utility.py (pro tier good design decision - maybe)
from utility import parse_ocr


st.set_page_config(page_title="Receipt OCR", layout="centered")

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
        # using gemini coz ocr only returns normal text and the possibilities of writing regex's for this situation are endless (trust me, i tried)
        formatted_ocr = (parse_ocr(text, image))
        
        #TODO
        # take the formatted ocr and write it down into expenses.csv with cols : Date, Description, Amount, Currency
        # formatted ocr will return a json object which looks like this; {"date": dd/mm/yyyy, "Description": "some description of what the expense was", "Amount": 4.00, "Currency": USD}
        # expenses.csv is in ../data/expenses.csv
    
    st.markdown("### 📝 Raw OCR Text")
    st.code(text)