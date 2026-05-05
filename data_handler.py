import pandas as pd
import os

FILE_NAME = "expenses.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

def add_expense(df, date, category, amount, description):
    new_entry = pd.DataFrame([{
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    return df

def delete_expense(df, index):
    df = df.drop(index).reset_index(drop=True)
    save_data(df)
    return df

def update_expense(df, index, date, category, amount, description):
    df.loc[index] = [date, category, amount, description]
    save_data(df)
    return df
