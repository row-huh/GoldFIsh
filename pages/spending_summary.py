import streamlit as st
from utility import load_expenses
from charts import generate_pie_chart, generate_bar_chart  # assuming you saved them in charts.py

st.set_page_config(page_title="Spending Summary", layout="wide")
st.title("📊 Spending Summary")

# 💅 Theme and Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f0f4f8, #dbe9f4);
        color: #2c3e50 !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] .css-1v0mbdj {
        color: #2c3e50 !important;
    }

    section[data-testid="stSidebar"] div[role="button"] {
        color: #2c3e50 !important;
    }

    section[data-testid="stSidebar"] div[role="button"]:hover {
        background-color: #d0f0fd !important;
        color: #0077b6 !important;
        font-weight: 700;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 📊 Load Data
expenses = load_expenses()
expenses = expenses[expenses["Amount"] > 0]  # Filter positive amounts only

if not expenses.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥧 Pie Chart")
        pie_fig = generate_pie_chart(expenses)
        st.pyplot(pie_fig)

    with col2:
        st.markdown("### 📊 Bar Chart")
        bar_fig = generate_bar_chart(expenses)
        st.pyplot(bar_fig)
else:
    st.info("📭 No data to display. Please add some expenses.")
