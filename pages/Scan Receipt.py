# implements ocr

import streamlit as st
from PIL import Image
import pytesseract
import io
import re
from datetime import datetime
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
        st.code(parse_ocr(text))
        

    st.markdown("### 📝 Raw OCR Text")
    st.code(text)



