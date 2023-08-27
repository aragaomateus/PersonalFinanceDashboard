import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import budget as bt
import cash_flow as cf
import src.investments as ivt 
st.set_page_config(page_title="Personal Finance Tracker",layout="wide")


def main():

    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Select a page", [ "Investments","Set Budget","Cash Flow"])
    
    if  page == "Cash Flow":
        st.title("Cash Flow")

        cf.show_cashFlow()
        
    elif page == "Set Budget":
        st.title("Budget")
        bt.show_budget()
        
        
    elif page == "Investments":
        st.title("Investments")
        ivt.show_investments()

if __name__ == "__main__":
    main()

