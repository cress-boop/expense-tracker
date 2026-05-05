import streamlit as st
import pandas as pd
import plotly.express as px
from data_handler import load_data, add_expense, delete_expense, update_expense
from utils import format_currency

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# SESSION LOGIN STATE
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN PAGE =================
if st.session_state.user is None:
    st.title("🔐 Login - Expense Tracker")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login / Register"):
        if username and password:
            st.session_state.user = username
            st.success(f"Welcome {username}!")
            st.rerun()
        else:
            st.warning("Please enter username and password")

# ================= MAIN APP =================
else:
    user = st.session_state.user

    st.title(f"💰 Smart Expense Tracker - {user}")

    # GROUP INFO
    st.markdown("""
    **Group 2**  
    • GALVEZ, MARY XIARIZ B  
    • ABELLON, BRANT ANTHONY B  
    • COLIGADO, Cristian C.  
    • JAMASALI, Arshad O  
    • SINGSON, FATIMA CEMILLE M.  
    """)

    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()

    df = load_data(user)

    # SIDEBAR INPUT
    st.sidebar.header("➕ Add Expense")

    date = st.sidebar.date_input("Date")
    category = st.sidebar.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Others"])
    amount = st.sidebar.number_input("Amount", min_value=0.0)
    description = st.sidebar.text_input("Description")

    if st.sidebar.button("Add Expense"):
        df = add_expense(df, user, str(date), category, amount, description)
        st.sidebar.success("Added!")

    # METRICS
    total = df["Amount"].sum()
    highest = df["Amount"].max() if not df.empty else 0
    count = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("💸 Total", format_currency(total))
    col2.metric("📈 Highest", format_currency(highest))
    col3.metric("🧾 Entries", count)

    st.markdown("---")

    # CHARTS
    if not df.empty:
        col4, col5 = st.columns(2)

        with col4:
            fig = px.pie(df, names="Category", values="Amount")
            st.plotly_chart(fig)

        with col5:
            df["Date"] = pd.to_datetime(df["Date"])
            trend = df.groupby("Date")["Amount"].sum().reset_index()
            fig2 = px.line(trend, x="Date", y="Amount")
            st.plotly_chart(fig2)

    # EDIT + DELETE
    st.subheader("📋 Manage Expenses")

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
        st.info("No data yet")
