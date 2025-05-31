import streamlit as st
import requests

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # Free API

def currency_converter():
    st.title("💱 Currency Converter")

    with st.spinner("Fetching latest exchange rates..."):
        try:
            response = requests.get(API_URL)
            data = response.json()
            rates = data["rates"]
        except Exception as e:
            st.error(f"Error fetching currency data: {e}")
            return

    currencies = sorted(rates.keys())

    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD"))
    with col2:
        to_currency = st.selectbox("To Currency", currencies, index=currencies.index("EUR"))

    amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.01, format="%.2f")

    if st.button("Convert"):
        if from_currency == to_currency:
            converted_amount = amount
        else:
            try:
                # Convert amount from "from_currency" to USD, then to "to_currency"
                usd_amount = amount / rates[from_currency]
                converted_amount = usd_amount * rates[to_currency]
            except KeyError:
                st.error("Currency not supported.")
                return

        st.success(f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")