import streamlit as st
import pandas as pd
import plotly.express as px
from data_handler import load_data, add_expense, delete_expense, update_expense
from utils import format_currency

# Page setup
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Custom UI style
st.markdown("""
<style>
.main {background-color: #0E1117;}
.group-box {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("💰 Smart Expense Tracker")

st.markdown("""
<div class="group-box">
<b>Group 2</b><br>
• GALVEZ, MARY XIARIZ B<br>
• ABELLON, BRANT ANTHONY B<br>
• COLIGADO, Cristian C.<br>
• JAMASALI, Arshad O<br>
• SINGSON, FATIMA CEMILLE M.
</div>
""", unsafe_allow_html=True)

st.caption("ITCC 103 – Final Examination | Python Web Application")

# Load data
df = load_data()

# SIDEBAR INPUT
st.sidebar.header("➕ Add Expense")

date = st.sidebar.date_input("Date")
category = st.sidebar.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Others"])
amount = st.sidebar.number_input("Amount", min_value=0.0)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    df = add_expense(df, str(date), category, amount, description)
    st.sidebar.success("Expense added!")

# METRICS
total = df["Amount"].sum()
highest = df["Amount"].max() if not df.empty else 0
count = len(df)

col1, col2, col3 = st.columns(3)
col1.metric("💸 Total Spent", format_currency(total))
col2.metric("📈 Highest Expense", format_currency(highest))
col3.metric("🧾 Transactions", count)

st.markdown("---")

# CHARTS
col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Expenses by Category")
    if not df.empty:
        fig = px.pie(df, names="Category", values="Amount", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

with col5:
    st.subheader("📈 Spending Trend")
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        trend = df.groupby("Date")["Amount"].sum().reset_index()
        fig2 = px.line(trend, x="Date", y="Amount", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

# MANAGE EXPENSES (EDIT + DELETE)
st.subheader("📋 Manage Expenses")

if not df.empty:
    for i, row in df.iterrows():
        with st.expander(f"{row['Category']} - {format_currency(row['Amount'])} ({row['Date']})"):

            col1, col2 = st.columns(2)

            if col1.button("🗑 Delete", key=f"delete_{i}"):
                df = delete_expense(df, i)
                st.rerun()

            if col2.button("✏ Edit", key=f"edit_{i}"):
                st.session_state[f"edit_{i}"] = True

            if st.session_state.get(f"edit_{i}", False):

                new_date = st.date_input("Date", value=pd.to_datetime(row["Date"]), key=f"d_{i}")
                new_category = st.selectbox("Category",
                                           ["Food", "Transport", "Bills", "Shopping", "Others"],
                                           index=["Food", "Transport", "Bills", "Shopping", "Others"].index(row["Category"]),
                                           key=f"c_{i}")
                new_amount = st.number_input("Amount", value=float(row["Amount"]), key=f"a_{i}")
                new_desc = st.text_input("Description", value=row["Description"], key=f"desc_{i}")

                if st.button("💾 Save Changes", key=f"s_{i}"):
                    df = update_expense(df, i, str(new_date), new_category, new_amount, new_desc)
                    st.session_state[f"edit_{i}"] = False
                    st.success("Updated!")
                    st.rerun()
else:
    st.info("No expenses yet.")

# FILTER
st.subheader("🔍 Filter")
categories = st.multiselect("Filter by Category", df["Category"].unique())

if categories:
    filtered = df[df["Category"].isin(categories)]
    st.dataframe(filtered, use_container_width=True)

# FOOTER
st.markdown("---")
st.caption("Developed by Group 2 | Tier 1 Streamlit Web Application")
