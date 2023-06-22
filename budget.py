import streamlit as st
import json
import os

def load_budget():
    if os.path.exists("budget.json"):
        with open("budget.json", "r") as f:
            return json.load(f)
    else:
        return {"Rent": 0, "Utilities": 0, "Groceries": 0, "Transportation": 0, "Health": 0, "Leisure": 0}

def save_budget(budget):
    with open("budget.json", "w") as f:
        json.dump(budget, f)

def show_budget():
    st.title("Budget")

    budget = load_budget()

    for category, amount in budget.items():
        budget[category] = st.number_input(f"{category} budget", value=amount)

    if st.button("Save budget"):
        save_budget(budget)
        st.success("Saved budget")
