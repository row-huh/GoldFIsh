import streamlit as st
from PIL import Image
import pytesseract
from pathlib import Path

def ocr_reader():
    st.title("🧾 Receipt OCR Scanner")
    st.caption("Upload your receipt image to extract text via OCR.")

    uploaded_file = st.file_uploader("Choose a receipt image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Receipt", use_column_width=True)

        with st.spinner("Extracting text with OCR..."):
            text = pytesseract.image_to_string(image)

        st.markdown("### 📝 Extracted Text")
        st.code(text)

    else:
        sample_path = Path("test-receipt.png")
        if sample_path.exists():
            image = Image.open(sample_path)
            st.image(image, caption="Sample Receipt (test-receipt.png)", use_column_width=True)
            with st.spinner("Extracting text with OCR from sample receipt..."):
                text = pytesseract.image_to_string(image)
            st.markdown("### 📝 Extracted Text from Sample Receipt")
            st.code(text)
        else:
            st.info("Please upload a receipt image file to get started.")