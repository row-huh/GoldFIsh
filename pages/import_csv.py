import streamlit as st
from data_manager import parse_bank_csv, save_expense

st.set_page_config(page_title="Import Bank CSV", layout="wide")

st.markdown("""
    <style>
    /* App background & font */
    .stApp {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        color: #333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 2rem 3rem 3rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f0f4f8, #dbe9f4);
        color: #2c3e50 !important;
        font-weight: 600;
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] div[role="button"] {
        color: #2c3e50 !important;
        padding: 0.7rem 1rem;
        border-radius: 8px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    section[data-testid="stSidebar"] div[role="button"]:hover {
        background-color: #d0f0fd !important;
        color: #0077b6 !important;
        font-weight: 700;
    }

    /* Page title style */
    .css-18e3th9 h1 {
        font-weight: 800;
        font-size: 3rem;
        color: #2980b9;
        margin-bottom: 1.5rem;
        letter-spacing: 0.05em;
    }

    /* File uploader container */
    .stFileUploader > div {
        background-color: #fff;
        border-radius: 12px;
        padding: 1rem;
        border: 1.8px solid #ccc;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        max-width: 480px;
        margin-bottom: 1.8rem;
    }

    /* Parsed CSV preview */
    .stDataFrame > div {
        border-radius: 12px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
        overflow-x: auto !important;
        margin-bottom: 2rem;
    }

    /* Import All button style */
    button[kind="primary"] {
        background: linear-gradient(to right, #36d1dc, #5b86e5);
        color: white;
        font-weight: 700;
        border-radius: 999px;
        padding: 0.8rem 2rem;
        border: none;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2);
        font-size: 1.15rem;
        transition: all 0.25s ease-in-out;
        margin-bottom: 2rem;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(to right, #1fa2ff, #5b86e5);
        transform: scale(1.05);
        box-shadow: 0 10px 28px rgba(0,0,0,0.3);
    }

    /* Success & error message style */
    .stSuccess > div, .stError > div {
        font-size: 1.1rem;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        max-width: 480px;
    }

    .stSuccess > div {
        background-color: #e6f4ea;
        color: #2e7d32;
        border-left: 6px solid #2ecc71;
    }

    .stError > div {
        background-color: #ffe6e6;
        color: #c62828;
        border-left: 6px solid #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📂 Import Bank CSV")

csv_file = st.file_uploader("📄 Upload your Bank CSV file", type=["csv"])

if csv_file:
    df_csv = parse_bank_csv(csv_file)

    if df_csv is not None and not df_csv.empty:
        st.markdown("### 📊 Parsed CSV Preview")
        st.dataframe(df_csv, use_container_width=True)

        if st.button("✅ Import All"):
            for _, row in df_csv.iterrows():
                save_expense(row["Date"], row["Description"], row["Amount"], "USD")
            st.success("🎉 Transactions imported successfully!")

            # Safe rerun with check:
            try:
                st.experimental_rerun()
            except AttributeError:
                pass  # rerun not supported, just continue

    else:
        st.error("❌ Failed to parse CSV or file is empty.")
