from datetime import datetime

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def format_currency(amount):
    return f"₱{amount:,.2f}"
