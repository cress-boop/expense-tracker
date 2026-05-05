import pandas as pd
import os

def get_file(username):
    return f"{username}_expenses.csv"

def load_data(username):
    file = get_file(username)
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(df, username):
    df.to_csv(get_file(username), index=False)

def add_expense(df, username, date, category, amount, description):
    new_entry = pd.DataFrame([{
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df, username)
    return df

def delete_expense(df, username, index):
    df = df.drop(index).reset_index(drop=True)
    save_data(df, username)
    return df

def update_expense(df, username, index, date, category, amount, description):
    df.loc[index] = [date, category, amount, description]
    save_data(df, username)
    return df
