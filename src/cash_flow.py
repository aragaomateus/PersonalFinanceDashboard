import streamlit as st
import json
import os
import pandas as pd
import altair as alt
import numpy as np 
import matplotlib.pyplot as plt

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors)])
    return fig

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
        
def load_surplus():
    if os.path.exists("surplus.json"):
        with open("surplus.json", "r") as f:
            return json.load(f)
    else:
        return []
    
def save_surplus(surplus):
    with open("surplus.json", "w") as f:
        json.dump(surplus, f)

def show_cashFlow():
    
    expenses = load_expenses()
    budget = load_budget()
    entries = load_entries()
    entries_df = pd.DataFrame(entries)
    entries_df['date'] = pd.to_datetime(entries_df['date'])
    entries_df['amount'] = pd.to_numeric(entries_df['amount'])
    
    if len(expenses) > 0:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])

        # Sidebar: Month selection
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = st.sidebar.selectbox('Select month', months, index=0)

        def filter_by_month(df, month):
            return df[df['date'].dt.month == month]
        
        month_number = months.index(month) + 1
        
        
        # Filter data by month
        data_month = filter_by_month(df, month_number)
        
        entries_month = filter_by_month(entries_df, month_number)
        
        total_entries = entries_month.amount.sum()
        
        # Calculate summary
        total_expense = data_month['amount'].sum()
        credit_total = data_month[data_month['payment_method'] == 'Credit Card']['amount'].sum()
        debit_total = data_month[data_month['payment_method'] == 'Debit Card']['amount'].sum()
        total_balance = total_entries - total_expense  
        
        surplus = load_surplus()
        
        def update_surplus(surplus,month,total_balance):
            for dic in surplus: 
                if dic["month"] == month: 
                    dic["surplus balance"] = total_balance
                    return surplus
            surplus.append({"month": month, "surplus balance":total_balance})
            return surplus
                    
        surplus = update_surplus(surplus,month,total_balance)
        save_surplus(surplus)
        

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
            st.pyplot(render_mpl_table(budget_expense_df, header_columns=0, col_width=1.7))
        
        st.subheader('Cash Flow Entries')

        type_of_entry = st.selectbox("Category", ["Money Entry", "Expense"])
        if type_of_entry == "Expense":
            st.header("Add expense")
            date_exp = st.date_input("Date")
            category = st.selectbox("Category", ["Rent", "Utilities", "Groceries", "Transportation", "Health", "Leisure"])
            payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card"])
            amount = st.number_input("Amount")

            if st.button("Add expense"):
                expenses.append({"date": date_exp.strftime("%Y-%m-%d"), "category": category, "payment_method": payment_method, "amount": amount})
                save_expenses(expenses)
                st.success("Added expense")
                
        elif type_of_entry == "Money Entry":
            
            st.header("Add Entry")
            date_sal = st.date_input("Date")
            payment_method = st.selectbox("Entry Method", ["Salary", "Extra"])
            amount = st.number_input("Amount")

            if st.button("Add Entry"):
                entries.append({"date": date_sal.strftime("%Y-%m-%d"), "payment_method": payment_method, "amount": amount})
                save_entries(entries)
                st.success("Added Entry")

        st.header("Expense Details")
        try:
            st.pyplot(render_mpl_table(data_month, header_columns=0, col_width=3.0))
        except:
            st.write("No data yet")
    # else:
    #     st.write("No expense data available yet.")
    #     st.header("Add expense")
        
    #     category = st.selectbox("Category", ["Rent", "Utilities", "Groceries", "Transportation", "Health", "Leisure"])
    #     payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card"])
    #     amount = st.number_input("Amount")

    #     if st.button("Add expense"):
    #         expenses.append({"date": date.strftime("%Y-%m-%d"), "category": category, "payment_method": payment_method, "amount": amount})
    #         save_expenses(expenses)
    #         st.success("Added expense")