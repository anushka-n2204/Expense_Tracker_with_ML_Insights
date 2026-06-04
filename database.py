"""
Database module for SQLite operations
Handles CRUD operations for expense tracking
"""
import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_path: str = "data/expenses.db"):
        """Initialize database connection and create table if not exists"""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create expenses table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                is_anomaly INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def add_expense(self, date: str, description: str, category: str, amount: float, is_anomaly: int = 0) -> int:
        """Add a new expense record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, description, category, amount, is_anomaly)
            VALUES (?, ?, ?, ?, ?)
        """, (date, description, category, amount, is_anomaly))
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return expense_id
    
    def get_all_expenses(self) -> pd.DataFrame:
        """Retrieve all expenses as a DataFrame"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
        conn.close()
        return df
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get expenses within a date range"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC"
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df
    
    def get_expenses_by_category(self, category: str) -> pd.DataFrame:
        """Get expenses filtered by category"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC"
        df = pd.read_sql_query(query, conn, params=(category,))
        conn.close()
        return df
    
    def update_expense(self, expense_id: int, date: str, description: str, category: str, amount: float):
        """Update an existing expense record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE expenses 
            SET date = ?, description = ?, category = ?, amount = ?
            WHERE id = ?
        """, (date, description, category, amount, expense_id))
        conn.commit()
        conn.close()
    
    def delete_expense(self, expense_id: int):
        """Delete an expense record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
    
    def update_anomaly_flag(self, expense_id: int, is_anomaly: int):
        """Update the anomaly flag for an expense"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET is_anomaly = ? WHERE id = ?", (is_anomaly, expense_id))
        conn.commit()
        conn.close()
    
    def get_expenses_last_n_days(self, days: int = 90) -> pd.DataFrame:
        """Get expenses from the last N days"""
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT * FROM expenses 
            WHERE date >= date('now', '-' || ? || ' days')
            ORDER BY date DESC
        """
        df = pd.read_sql_query(query, conn, params=(days,))
        conn.close()
        return df
    
    def get_category_totals(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """Get total spending by category"""
        conn = sqlite3.connect(self.db_path)
        if start_date and end_date:
            query = """
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE date BETWEEN ? AND ?
                GROUP BY category
                ORDER BY total DESC
            """
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        else:
            query = """
                SELECT category, SUM(amount) as total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
            """
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_monthly_totals(self, months: int = 6) -> pd.DataFrame:
        """Get total spending by month for the last N months"""
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM expenses
            WHERE date >= date('now', '-' || ? || ' months')
            GROUP BY month
            ORDER BY month
        """
        df = pd.read_sql_query(query, conn, params=(months,))
        conn.close()
        return df
