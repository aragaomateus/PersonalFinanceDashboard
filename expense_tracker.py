
import streamlit as st
import pandas as pd
import altair as alt
# def expense_summary():
#     # Load the data from a CSV file
#     df = dummy_data.make_dummy_data()
#     df['date'] = pd.to_datetime(df['date'])

#     def filter_by_month(df, month):
#         return df[df['date'].dt.month == month]

#     # Sidebar: Month selection
#     month = st.sidebar.selectbox('Select month', range(1, 13), index=0)

#     # Main: Display summary and chart
#     st.title('Expense Tracker')

#     # Filter data by month
#     data_month = filter_by_month(df, month)

#     # Calculate summary
#     credit_total = data_month['credit card'].sum()
#     debit_total = data_month['debit card'].sum()
#     balance = credit_total + debit_total
#     salary = 5000

#     # Define the Streamlit app
#     st.title('Expense Summary')

#     # Column 1: Initial summary
#     st.subheader('Summary')
#     col1, col2 = st.columns(2)
#     box_color = 'green' if balance >= 0 else 'red'
#     box = f"""
#     <div style="background-color: {box_color}; padding: 10px; border-radius: 5px">
#         <h3 style="color: white">Summary</h3>
#         <p style="color: white">Credit card total: {credit_total}</p>
#         <p style="color: white">Debit card total: {debit_total}</p>
#         <hr style="border: none; height: 2px; background-color: white">
#         <p style="color: white; font-weight: bold">Balance: {balance}</p>
#     </div>
#     """
#     col1.markdown(box, unsafe_allow_html=True)

#     # Column 2: Line chart of expenses by week
#     with col2:
#         st.subheader('Expenses by Week')
#         df["date"] = pd.to_datetime(df["date"])
#         expenses_by_week = df.groupby(pd.Grouper(key='date', freq='W-MON'))[['credit card', 'debit card']].sum().reset_index()
#         expenses_by_week['Week'] = expenses_by_week['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
#         expenses_by_week['Total Expenses'] = expenses_by_week['credit card'] + expenses_by_week['debit card']
#         chart = alt.Chart(expenses_by_week).mark_line().encode(
#             x='Week:T',
#             y='Total Expenses:Q'
#         ).properties(
#             width=600,
#             height=300
#         )
#         st.altair_chart(chart)
