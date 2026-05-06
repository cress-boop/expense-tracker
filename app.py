import streamlit as st
import pandas as pd
import plotly.express as px
from data_handler import load_data, add_expense, delete_expense, update_expense
from utils import format_currency
from auth import register_user, login_user

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# SESSION STATE
if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# ================= LOGIN =================
if st.session_state.user is None:

    if menu == "Login":
        st.title("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.user = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("❌ Wrong username or password")

    # ================= REGISTER =================
    elif menu == "Register":
        st.title("📝 Register")

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created! You can now login.")
            else:
                st.error("⚠ Username already exists")

# ================= MAIN APP =================
else:
    user = st.session_state.user

    st.title(f"💰 Expense Tracker - {user}")

    # PROFILE VIEW
    st.subheader("👤 Profile")
    st.write(f"Username: **{user}**")

    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()

    # GROUP INFO
    st.markdown("""
    **Group 2**  
    • GALVEZ, MARY XIARIZ B  
    • ABELLON, BRANT ANTHONY B  
    • COLIGADO, Cristian C.  
    • JAMASALI, Arshad O  
    • SINGSON, FATIMA CEMILLE M.  
    """)

    df = load_data(user)

    # ADD EXPENSE
    st.sidebar.header("➕ Add Expense")

    date = st.sidebar.date_input("Date")
    category = st.sidebar.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Others"])
    amount = st.sidebar.number_input("Amount", min_value=0.0)
    description = st.sidebar.text_input("Description")

    if st.sidebar.button("Add"):
        df = add_expense(df, user, str(date), category, amount, description)
        st.sidebar.success("Added!")

    # METRICS
    total = df["Amount"].sum()
    st.metric("💸 Total Expenses", format_currency(total))

    # CHART
    if not df.empty:
        fig = px.pie(df, names="Category", values="Amount")
        st.plotly_chart(fig)

    # EDIT / DELETE
    st.subheader("📋 Your Expenses")

    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"{row['Category']} - {format_currency(row['Amount'])}"):

                col1, col2 = st.columns(2)

                if col1.button("Delete", key=f"d_{i}"):
                    df = delete_expense(df, user, i)
                    st.rerun()

                if col2.button("Edit", key=f"e_{i}"):
                    st.session_state[f"edit_{i}"] = True

                if st.session_state.get(f"edit_{i}", False):
                    new_date = st.date_input("Date", value=pd.to_datetime(row["Date"]), key=f"date_{i}")
                    new_cat = st.selectbox("Category",
                                           ["Food", "Transport", "Bills", "Shopping", "Others"],
                                           key=f"cat_{i}")
                    new_amt = st.number_input("Amount", value=float(row["Amount"]), key=f"amt_{i}")
                    new_desc = st.text_input("Description", value=row["Description"], key=f"desc_{i}")

                    if st.button("Save", key=f"s_{i}"):
                        df = update_expense(df, user, i, str(new_date), new_cat, new_amt, new_desc)
                        st.session_state[f"edit_{i}"] = False
                        st.rerun()
    else:
        st.info("No expenses yet")
