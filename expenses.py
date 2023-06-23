import streamlit as st
import json
import os
import pandas as pd
import altair as alt
def load_entries():
    if os.path.exists("entries.json"):
        with open("entries.json", "r") as f:
            return json.load(f)
    else:
        return []

def save_entries(entries):
    with open("entries.json", "w") as f:
        json.dump(entries, f)
def load_expenses():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            return json.load(f)
    else:
        return []

def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f)

def load_budget():
    if os.path.exists("budget.json"):
        with open("budget.json", "r") as f:
            return json.load(f)
    else:
        return {}

def save_budget(budget):
    with open("budget.json", "w") as f:
        json.dump(budget, f)

def show_expenses():
    
    expenses = load_expenses()
    budget = load_budget()

    if len(expenses) > 0:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])

        # Sidebar: Month selection
        month = st.sidebar.selectbox('Select month', range(1, 13), index=0)

        def filter_by_month(df, month):
            return df[df['date'].dt.month == month]

        # Filter data by month
        data_month = filter_by_month(df, month)

        # Calculate summary
        total_expense = data_month['amount'].sum()
        credit_total = data_month[data_month['payment_method'] == 'Credit Card']['amount'].sum()
        debit_total = data_month[data_month['payment_method'] == 'Debit Card']['amount'].sum()
        total_balance = 5000 - total_expense  # assuming 5000 as salary

        st.subheader('Summary')
        col1, col2 = st.columns(2)
        box_color = 'green' if total_balance >= 0 else 'red'
        box = f"""
        <div style="background-color: {box_color}; padding: 10px; border-radius: 5px">
            <h3 style="color: white">Summary</h3>
            <p style="color: white">Total expense: {total_expense}</p>
            <p style="color: white">Credit Card: {credit_total}</p>
            <p style="color: white">Debit Card: {debit_total}</p>
            <hr style="border: none; height: 2px; background-color: white">
            <p style="color: white; font-weight: bold">Balance: {total_balance}</p>
        </div>
        """
        col1.markdown(box, unsafe_allow_html=True)

        st.subheader('Expenses by Category')
        expenses_by_category = data_month.groupby('category')['amount'].sum().reset_index()
        expenses_by_category['percent'] = expenses_by_category['amount'] / expenses_by_category['amount'].sum() * 100
        chart = alt.Chart(expenses_by_category).mark_bar().encode(
            x='category:N',
            y='amount:Q',
            tooltip=['category', 'amount', alt.Tooltip('percent:Q', format='.1f')]
        ).properties(
            width=600,
            height=300
        )
        st.altair_chart(chart)

        # Display the budget, expense and balance
        budget_df = pd.DataFrame(list(budget.items()), columns=['category', 'budget'])
        budget_expense_df = pd.merge(budget_df, expenses_by_category, how='left', on='category').fillna(0)
        budget_expense_df = budget_expense_df.drop(columns="percent")
        budget_expense_df['remaining'] = budget_expense_df['budget'] - budget_expense_df['amount']
        with col2:
            st.subheader('Budget')
            st.write(budget_expense_df)
        
        '''FIXME
        make it so we can decide with an if statement which type of entry it is
        then it will take to the right widgets.
        
        '''
        
        col3, col4 = st.columns(2)
        with col3:
            st.header("Add expense")
            date_exp = st.date_input("Date")
            category = st.selectbox("Category", ["Rent", "Utilities", "Groceries", "Transportation", "Health", "Leisure"])
            payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card"])
            amount = st.number_input("Amount")

            if st.button("Add expense"):
                expenses.append({"date": date_exp.strftime("%Y-%m-%d"), "category": category, "payment_method": payment_method, "amount": amount})
                save_expenses(expenses)
                st.success("Added expense")
                
        with col4:
            st.header("Add Entry")
            date_sal = st.date_input("Date")
            payment_method = st.selectbox("Entry Method", ["Salary", "Extra"])
            amount = st.number_input("Amount")

            if st.button("Add Entry"):
                expenses.append({"date": date_sal.strftime("%Y-%m-%d"), "category": category, "payment_method": payment_method, "amount": amount})
                save_expenses(expenses)
                st.success("Added expense")

        st.header("Expense Details")
        st.dataframe(data_month)

    else:
        st.write("No expense data available yet.")
        st.header("Add expense")
        
        category = st.selectbox("Category", ["Rent", "Utilities", "Groceries", "Transportation", "Health", "Leisure"])
        payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card"])
        amount = st.number_input("Amount")

        if st.button("Add expense"):
            expenses.append({"date": date.strftime("%Y-%m-%d"), "category": category, "payment_method": payment_method, "amount": amount})
            save_expenses(expenses)
            st.success("Added expense")