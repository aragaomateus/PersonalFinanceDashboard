import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import expense_tracker as et 
import budget as bt
import expenses as exp
st.set_page_config(page_title="Personal Finance Tracker")

def get_stock_data(ticker_symbol, start_date, end_date):
    ticker_data = yf.Ticker(ticker_symbol)
    ticker_df = ticker_data.history(period='1mo', start=start_date, end=end_date)
    return ticker_df, ticker_data.fast_info

def load_portfolio(portfolio_file):
    if os.path.exists(portfolio_file):
        with open(portfolio_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_portfolio(portfolio, portfolio_file):
    with open(portfolio_file, "w") as f:
        json.dump(portfolio, f)

def main():

    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Select a page", [ "Investments","Set Budget","Cash Flow"])
    
    if  page == "Cash Flow":
        st.title("Cash Flow")

        exp.show_expenses()
        
    elif page == "Set Budget":
        st.title("Budget")
        bt.show_budget()
        
        
    elif page == "Investments":
        st.title("Investments")
        
        portfolio_file = "stock_portfolio.json"
        portfolio = load_portfolio(portfolio_file)

        for ticker_symbol, stock_info in portfolio.items():
            df, info = get_stock_data(ticker_symbol, stock_info["start_date"], stock_info["end_date"])
            st.header(ticker_symbol)
            st.subheader("Fundamentals")
            st.write(info)

            st.subheader("Performance")
            st.line_chart(df['Close'])

            if not df.empty:
                current_price = df['Close'].iloc[-1]
                num_shares = stock_info["num_shares"]
                avg_cost = stock_info["avg_cost"]
                total_spent = num_shares * avg_cost
                total_value = num_shares * current_price
                profit_loss = total_value - total_spent

                st.write(f"Current Price: {current_price}")
                st.write(f"Total Spent: {total_spent}")
                st.write(f"Total Value: {total_value}")
                st.write(f"Profit/Loss: {profit_loss}")

        st.sidebar.header("Add Stock")
        ticker_symbol = st.sidebar.text_input("Enter Ticker Symbol")
        start_date = st.sidebar.date_input("Start date")
        end_date = st.sidebar.date_input("End date")
        num_shares = st.sidebar.number_input("Number of shares", step=1)
        avg_cost = st.sidebar.number_input("Average cost per share")

        if st.sidebar.button("Save to Stock Portfolio"):
            portfolio = load_portfolio(portfolio_file)
            portfolio[ticker_symbol] = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "num_shares": num_shares,
                "avg_cost": avg_cost
            }
            save_portfolio(portfolio, portfolio_file)
            st.success("Saved to stock portfolio")

if __name__ == "__main__":
    main()

