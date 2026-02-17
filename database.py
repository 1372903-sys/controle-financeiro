import sqlite3
import pandas as pd
import hashlib
import random
import string
from datetime import datetime, timedelta

DB_NAME = "finance_control.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Recuperação de Senha
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL
        )
    ''')
    
    # Tabelas Financeiras com user_id obrigatório
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source_name TEXT NOT NULL,
            value REAL NOT NULL,
            category TEXT DEFAULT 'Geral',
            is_recurring INTEGER DEFAULT 0,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            value REAL NOT NULL,
            category TEXT NOT NULL,
            is_recurring INTEGER DEFAULT 0,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'Geral',
            is_recurring INTEGER DEFAULT 0,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Tabela de Metas Financeiras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            target_value REAL NOT NULL,
            current_value REAL DEFAULT 0,
            deadline DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Funções de Usuário ---
def create_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email_or_user, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE (email = ? OR username = ?) AND password = ?", 
                   (email_or_user, email_or_user, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user if user else None

# --- Recuperação de Senha ---
def generate_reset_code(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if not cursor.fetchone():
        conn.close()
        return None
    code = ''.join(random.choices(string.digits, k=6))
    expires_at = datetime.now() + timedelta(minutes=15)
    cursor.execute("INSERT INTO password_resets (email, code, expires_at) VALUES (?, ?, ?)", 
                   (email, code, expires_at))
    conn.commit()
    conn.close()
    return code

def verify_reset_code(email, code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM password_resets WHERE email = ? AND code = ? AND expires_at > ?", 
                   (email, code, datetime.now()))
    reset = cursor.fetchone()
    conn.close()
    return True if reset else False

def reset_password(email, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hash_password(new_password), email))
    cursor.execute("DELETE FROM password_resets WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    return True

# --- Funções de Dados (ISOLAMENTO GARANTIDO POR user_id) ---

def add_income(user_id, source, value, category, month, year, is_recurring=0):
    conn = get_connection()
    cursor = conn.cursor()
    for i in range(12 if is_recurring else 1):
        m = (month + i - 1) % 12 + 1
        y = year + (month + i - 1) // 12
        cursor.execute("INSERT INTO incomes (user_id, source_name, value, category, is_recurring, month, year) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (user_id, source, value, category, is_recurring, m, y))
    conn.commit()
    conn.close()

def get_incomes(user_id, month, year):
    conn = get_connection()
    # Filtro obrigatório por user_id para evitar vazamento de dados
    df = pd.read_sql_query("SELECT * FROM incomes WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, month, year))
    conn.close()
    return df

def delete_income(income_id, user_id, delete_all_recurring=False, source_name=None):
    conn = get_connection()
    cursor = conn.cursor()
    if delete_all_recurring and source_name:
        # Garante que só deleta itens do próprio usuário
        cursor.execute("DELETE FROM incomes WHERE user_id = ? AND source_name = ? AND is_recurring = 1", (user_id, source_name))
    else:
        # Garante que só deleta o ID se pertencer ao usuário
        cursor.execute("DELETE FROM incomes WHERE id = ? AND user_id = ?", (income_id, user_id))
    conn.commit()
    conn.close()

def add_expense(user_id, description, value, category, month, year, is_recurring=0):
    conn = get_connection()
    cursor = conn.cursor()
    for i in range(12 if is_recurring else 1):
        m = (month + i - 1) % 12 + 1
        y = year + (month + i - 1) // 12
        cursor.execute("INSERT INTO expenses (user_id, description, value, category, is_recurring, month, year) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (user_id, description, value, category, is_recurring, m, y))
    conn.commit()
    conn.close()

def get_expenses(user_id, month, year):
    conn = get_connection()
    # Filtro obrigatório por user_id
    df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, month, year))
    conn.close()
    return df

def delete_expense(expense_id, user_id, delete_all_recurring=False, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    if delete_all_recurring and description:
        cursor.execute("DELETE FROM expenses WHERE user_id = ? AND description = ? AND is_recurring = 1", (user_id, description))
    else:
        cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    conn.commit()
    conn.close()

def add_investment(user_id, amount, category, month, year, is_recurring=0):
    conn = get_connection()
    cursor = conn.cursor()
    for i in range(12 if is_recurring else 1):
        m = (month + i - 1) % 12 + 1
        y = year + (month + i - 1) // 12
        cursor.execute("INSERT INTO investments (user_id, amount, category, is_recurring, month, year) VALUES (?, ?, ?, ?, ?, ?)", 
                       (user_id, amount, category, is_recurring, m, y))
    conn.commit()
    conn.close()

def get_investments(user_id, month, year):
    conn = get_connection()
    # Filtro obrigatório por user_id
    df = pd.read_sql_query("SELECT * FROM investments WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, month, year))
    conn.close()
    return df

def delete_investment(inv_id, user_id, delete_all_recurring=False, category=None):
    conn = get_connection()
    cursor = conn.cursor()
    if delete_all_recurring and category:
        cursor.execute("DELETE FROM investments WHERE user_id = ? AND category = ? AND is_recurring = 1", (user_id, category))
    else:
        cursor.execute("DELETE FROM investments WHERE id = ? AND user_id = ?", (inv_id, user_id))
    conn.commit()
    conn.close()

def get_annual_summary(user_id, year):
    conn = get_connection()
    # Todas as agregações filtradas por user_id
    incomes = pd.read_sql_query("SELECT value, month FROM incomes WHERE user_id = ? AND year = ?", conn, params=(user_id, year))
    expenses = pd.read_sql_query("SELECT value, month FROM expenses WHERE user_id = ? AND year = ?", conn, params=(user_id, year))
    investments = pd.read_sql_query("SELECT amount, month FROM investments WHERE user_id = ? AND year = ?", conn, params=(user_id, year))
    conn.close()
    return incomes, expenses, investments

def get_future_projection(user_id, start_month, start_year, periods=12):
    conn = get_connection()
    results = []
    current_m, current_y = start_month, start_year
    for _ in range(periods):
        # Filtros por user_id garantidos em cada mês da projeção
        inc = pd.read_sql_query("SELECT SUM(value) as total FROM incomes WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, current_m, current_y))['total'].iloc[0] or 0.0
        exp = pd.read_sql_query("SELECT SUM(value) as total FROM expenses WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, current_m, current_y))['total'].iloc[0] or 0.0
        inv = pd.read_sql_query("SELECT SUM(amount) as total FROM investments WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, current_m, current_y))['total'].iloc[0] or 0.0
        results.append({
            "Mês": current_m, 
            "Ano": current_y, 
            "Receita": inc, 
            "Despesa": exp, 
            "Investimento": inv, 
            "Saldo": inc - exp
        })
        current_m += 1
        if current_m > 12:
            current_m = 1
            current_y += 1
    conn.close()
    return pd.DataFrame(results)

# --- Funções de Metas ---
def add_goal(user_id, name, target_value, deadline=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO goals (user_id, name, target_value, deadline) VALUES (?, ?, ?, ?)", 
                   (user_id, name, target_value, deadline))
    conn.commit()
    conn.close()

def get_goals(user_id):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM goals WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return df

def update_goal_progress(goal_id, user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE goals SET current_value = current_value + ? WHERE id = ? AND user_id = ?", 
                   (amount, goal_id, user_id))
    conn.commit()
    conn.close()

def delete_goal(goal_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id))
    conn.commit()
    conn.close()
