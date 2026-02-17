import pandas as pd

def format_currency(value):
    """Formata um valor numérico para o padrão de moeda brasileiro R$ 0.000,00"""
    if value is None:
        value = 0.0
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate_monthly_totals(incomes_df, expenses_df, investment_val):
    total_income = incomes_df['value'].sum() if not incomes_df.empty else 0.0
    total_expense = expenses_df['value'].sum() if not expenses_df.empty else 0.0
    balance = total_income - total_expense
    return total_income, total_expense, balance, investment_val
