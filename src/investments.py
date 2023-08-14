import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import constants as const 
import json
import os

def get_investment_allocation(total_investment, stock_percentage, etf_percentage, etf_spy_percentage, num_stocks, num_etfs):
    etf_spy_allocation = total_investment * etf_percentage * etf_spy_percentage
    other_etfs_allocation = (total_investment * etf_percentage - etf_spy_allocation) / (num_etfs - 1)
    stock_allocation = (total_investment * stock_percentage) / num_stocks

    return etf_spy_allocation, other_etfs_allocation, stock_allocation
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

def calculate_portfolio_value(portfolio):
    portfolio_value_df = pd.DataFrame()

    for ticker_symbol, stock_info in portfolio.items():
        df, _ = get_stock_data(ticker_symbol, stock_info["start_date"], stock_info["end_date"])
        df = df.loc[:, ['Close']]
        df = df * stock_info["num_shares"]
        portfolio_value_df[ticker_symbol] = df['Close']

    portfolio_value_df['Total'] = portfolio_value_df.sum(axis=1)
    return portfolio_value_df

key=const.API_KEY

import financetoolkit as tool

def get_price(stocks):
    data = tool.Toolkit(stocks,api_key=key)
    return data.get_historical_data()['Close'].tail(1).values[0]

def calculate_portfolio_values(portfolio):
        total_spent = 0
        total_current_value = 0

        for ticker_symbol, stock_info in portfolio.items():
            current_price = get_price(ticker_symbol)
            total_spent += stock_info["num_shares"] * stock_info["avg_cost"]
            total_current_value += stock_info["num_shares"] * current_price

        profit_loss = total_current_value - total_spent

        return total_spent, total_current_value, profit_loss

def show_investments():
    portfolio_file = "stock_portfolio.json"
    portfolio = load_portfolio(portfolio_file)
    # Create an empty DataFrame to store portfolio data
    portfolio_df = pd.DataFrame(columns=['Ticker', 'Total Value'])
    assest_class = {}

# Calculate values
    total_spent, total_current_value, profit_loss = calculate_portfolio_values(portfolio)

    # Display values
    st.subheader("Portfolio Summary")
    st.markdown(f"**Total Cost (Spent on purchases):** ${total_spent:,.2f}")
    st.markdown(f"**Current Value of Portfolio:** ${total_current_value:,.2f}")
    st.markdown(f"**Profit/Loss:** ${profit_loss:,.2f}")

    if profit_loss > 0:
        st.markdown(f"📈 Your portfolio has gained in value by ${profit_loss:,.2f}")
    else:
        st.markdown(f"📉 Your portfolio has decreased in value by ${-profit_loss:,.2f}")
    
    
    df = pd.DataFrame.from_dict(portfolio, orient='index').reset_index()
    df.rename(columns={'index': 'Ticker'}, inplace=True)
    df['Total Value'] = df['num_shares'] * df['avg_cost']
    total_values = df.groupby('class')['Total Value'].sum().reset_index()
    
    
    #populating the df for the stack information to be shown in the pie graph
    for ticker_symbol, stock_info in portfolio.items():
            # Append the total value of this stock to the portfolio DataFrame
        new_row = pd.DataFrame({"Ticker": [ticker_symbol], "Total Value": stock_info['num_shares']*stock_info['avg_cost']})
        portfolio_df = pd.concat([portfolio_df, new_row], ignore_index=True)  
        
    #populating the df for the assest class 
        
    col1, col2 = st.columns(2)
    
    with col1:
        # Plot a pie chart of the portfolio
        st.subheader("Portfolio Overview")
        fig = px.pie(portfolio_df, values='Total Value', names='Ticker', title='Portfolio Holdings', 
                    width=600, height=400)  # You can adjust these values as needed
        fig.update_layout(legend=dict(x=-0.1, y=0.5))
        st.plotly_chart(fig)
        
    with col2:
        st.subheader("Asset Class Difference")
        fig = px.pie(total_values, values='Total Value', names='class', title='Percentage of Stocks and ETFs')
        st.plotly_chart(fig)
        
    # Allow adding more stocks
    st.header("Add Stock")
    ticker_symbol = st.text_input("Enter Ticker Symbol").upper()
    num_shares = st.number_input("Number of shares")
    avg_cost = st.number_input("Average cost per share")

    if st.button("Save to Stock Portfolio"):
        portfolio = load_portfolio(portfolio_file)
        if ticker_symbol in portfolio:
            old_shares = portfolio[ticker_symbol]["num_shares"]
            old_avg_cost = portfolio[ticker_symbol]["avg_cost"]
            
            # Compute new average cost and update shares
            total_cost_old = old_shares * old_avg_cost
            total_cost_new = num_shares * avg_cost
            total_shares = old_shares + num_shares
            
            new_avg_cost = (total_cost_old + total_cost_new) / total_shares
            new_shares = old_shares + num_shares

            portfolio[ticker_symbol] = {
                "num_shares": new_shares,
                "avg_cost": new_avg_cost
            }
        else:
            portfolio[ticker_symbol] = {
                "num_shares": num_shares,
                "avg_cost": avg_cost
            }
        save_portfolio(portfolio, portfolio_file)
        st.success("Saved to stock portfolio")
        
    st.title("Investment Allocation Calculator")

    # user input
    total_investment = st.number_input('Enter your total monthly investment', value=250.0)
    stock_percentage = st.slider('Enter your stock allocation percentage', 0.0, 1.0, 0.6)
    etf_percentage = st.slider('Enter your ETF allocation percentage', 0.0, 1.0, 0.4)
    etf_spy_percentage = st.slider('Enter your SPY allocation percentage within ETFs', 0.0, 1.0, 0.5)
    num_stocks = st.number_input('Enter the number of different stocks you invest in', value=4, step=1)
    num_etfs = st.number_input('Enter the number of different ETFs you invest in', value=5, step=1)

    # calculate allocations
    etf_spy_allocation, other_etfs_allocation, stock_allocation = get_investment_allocation(total_investment, stock_percentage, etf_percentage, etf_spy_percentage, num_stocks, num_etfs)

    st.write(f"Monthly investment in SPY: ${etf_spy_allocation:.2f}")
    st.write(f"Monthly investment in each of the other ETFs: ${other_etfs_allocation:.2f}")
    st.write(f"Monthly investment in each stock: ${stock_allocation:.2f}")