"""
Utility functions for the expense tracker
Includes date helpers and CSV export
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def get_current_month_range() -> tuple:
    """Get start and end date of current month"""
    today = datetime.now()
    start_date = today.replace(day=1).strftime('%Y-%m-%d')
    
    # Get last day of month
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    
    end_date = (next_month - timedelta(days=1)).strftime('%Y-%m-%d')
    
    return start_date, end_date


def get_last_n_months_range(n: int = 6) -> tuple:
    """Get start and end date for last N months"""
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    
    # Calculate start date
    start_date = (today - timedelta(days=n*30)).strftime('%Y-%m-%d')
    
    return start_date, end_date


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"₹{amount:,.2f}"


def export_to_csv(df: pd.DataFrame, filename: str = "expenses_export.csv") -> str:
    """
    Export expenses DataFrame to CSV
    
    Args:
        df: DataFrame with expense data
        filename: Output filename
        
    Returns:
        Path to exported file
    """
    # Select and rename columns for export
    export_df = df[['date', 'description', 'category', 'amount', 'is_anomaly']].copy()
    export_df.rename(columns={
        'date': 'Date',
        'description': 'Description',
        'category': 'Category',
        'amount': 'Amount',
        'is_anomaly': 'Flagged'
    }, inplace=True)
    
    # Convert flagged to Yes/No
    export_df['Flagged'] = export_df['Flagged'].apply(lambda x: 'Yes' if x == 1 else 'No')
    
    # Export
    export_df.to_csv(filename, index=False)
    
    return filename


def validate_date(date_string: str) -> bool:
    """Validate date string format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_amount(amount: float) -> bool:
    """Validate amount is positive"""
    return amount > 0


def get_month_name(date_string: str) -> str:
    """Get month name from date string"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%B %Y')
    except:
        return date_string


def calculate_budget_percentage(spent: float, budget: float) -> float:
    """Calculate percentage of budget used"""
    if budget <= 0:
        return 0.0
    return (spent / budget) * 100
