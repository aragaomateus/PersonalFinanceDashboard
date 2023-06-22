import streamlit as st
import json
import os

def load_expenses():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            return json.load(f)
    else:
        return []

def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f)

def show_expenses():
    st.title("Expenses")

    expenses = load_expenses()

    for expense in expenses:
        st.write(f"{expense['date']}: {expense['category']}, {expense['amount']}")

    st.header("Add expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Rent", "Utilities", "Groceries", "Transportation", "Health", "Leisure"])
    amount = st.number_input("Amount")

    if st.button("Add expense"):
        expenses.append({"date": date.strftime("%Y-%m-%d"), "category": category, "amount": amount})
        save_expenses(expenses)
        st.success("Added expense")
