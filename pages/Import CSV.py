import streamlit as st
from utility import parse_bank_csv, save_expense

st.set_page_config(page_title="Import Bank CSV", layout="wide")

# Unified Dashboard Styling - matching purple theme
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
    
    /* Caption styling */
    .stCaption p {
        color: #E2E8F0 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        max-width: 600px !important;
        margin: 2rem auto !important;
    }
    
    .stFileUploader > div:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(168, 85, 247, 0.6) !important;
        transform: translateY(-2px);
    }
    
    .stFileUploader label {
        color: #fff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Hide file uploader additional elements */
    .stFileUploader > div > div:last-child {
        display: none !important;
    }
    
    .stFileUploader [data-testid="fileUploaderFileInput"] + div {
        display: none !important;
    }
    
    .stFileUploader small {
        display: none !important;
    }
    
    /* DataFrame styling */
    .stDataFrame > div {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
        overflow: hidden !important;
        margin: 2rem auto !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    
    /* DataFrame table styling */
    .stDataFrame table {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #333 !important;
    }
    
    .stDataFrame th {
        background: rgba(124, 58, 237, 0.2) !important;
        color: #333 !important;
        font-weight: 700 !important;
    }
    
    /* Import All button style */
    button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 15px !important;
        padding: 1rem 2.5rem !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        margin: 2rem auto !important;
        display: block !important;
        min-width: 250px !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #9333ea 50%, #a855f7 100%) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(124, 58, 237, 0.6) !important;
    }
    
    /* Success & error message style */
    .stSuccess > div {
        background: rgba(34, 197, 94, 0.15) !important;
        color: #22c55e !important;
        border: 1px solid #22c55e !important;
        border-radius: 12px !important;
        padding: 1.2rem 1.8rem !important;
        margin: 1.5rem auto !important;
        max-width: 600px !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
        font-weight: 600 !important;
    }
    
    .stError > div {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #ef4444 !important;
        border: 1px solid #ef4444 !important;
        border-radius: 12px !important;
        padding: 1.2rem 1.8rem !important;
        margin: 1.5rem auto !important;
        max-width: 600px !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
        font-weight: 600 !important;
    }
    
    /* Section headers */
    h3 {
        color: #fff !important;
        text-align: center !important;
        font-weight: 700 !important;
        margin: 2rem 0 1rem 0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
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
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📂 Import Bank CSV</h1>', unsafe_allow_html=True)
st.caption("Upload your bank CSV file to automatically import transactions.")

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