import random
from datetime import date, timedelta
import pandas as pd

def make_dummy_data():

    # Generate random dates for the last 6 months
    today = date.today()
    dates = [today - timedelta(days=random.randint(0, 180)) for i in range(20)]

    # Define the categories and descriptions
    categories = ['Groceries', 'Transportation', 'Entertainment', 'Utilities', 'Salary', 'Shopping']
    descriptions = ['Supermarket ABC', 'Gas station XYZ', 'Movie tickets for two', 'Electricity bill', 'Online shopping']

    # Generate the dummy data
    data = []
    for i in range(20):
        category = random.choice(categories)
        description = random.choice(descriptions)
        cc_amount = round(random.uniform(-100, 100), 2)
        dc_amount = round(random.uniform(-100, 100), 2)
        data.append({'date': str(dates[i]), 'category': category, 'description': description,
                    'credit card': cc_amount, 'debit card': dc_amount})

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Show the first few rows of the DataFrame
    return df
    
data = make_dummy_data()
data['date'] = pd.to_datetime(data['date'])
print(data['date'].dt.month)


