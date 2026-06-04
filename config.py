"""
Configuration file for the expense tracker
"""

# Application settings
APP_NAME = "Smart Expense Tracker"
VERSION = "1.0"
INSTITUTION = "SRM Institute of Science and Technology, KTR"

# Database settings
DATABASE_PATH = "data/expenses.db"
TRAINING_DATA_PATH = "data/training_data.csv"

# Model settings
MODEL_PATH = "models/categorizer.pkl"
CATEGORIES = [
    "Food",
    "Transport", 
    "Shopping",
    "Utilities",
    "Health",
    "Entertainment",
    "Education",
    "Other"
]

# ML settings
MODEL_MAX_FEATURES = 500
MODEL_NGRAM_RANGE = (1, 2)
MODEL_TEST_SIZE = 0.2
MODEL_RANDOM_STATE = 42
TARGET_ACCURACY = 0.85

# Anomaly detection settings
ANOMALY_CONTAMINATION = 0.05
ANOMALY_LOOKBACK_DAYS = 90
ANOMALY_MIN_SAMPLES = 10
ANOMALY_STD_THRESHOLD = 2.0

# Budget settings
DEFAULT_MONTHLY_BUDGET = 10000.0
BUDGET_WARNING_THRESHOLD = 0.80  # 80%
BUDGET_ALERT_THRESHOLD = 1.00    # 100%

# UI settings
CHART_HEIGHT = 400
TABLE_PAGE_SIZE = 100
DATE_FORMAT = "%Y-%m-%d"
CURRENCY_SYMBOL = "₹"

# Export settings
EXPORT_FILENAME = "expenses_export.csv"
EXPORT_COLUMNS = ['date', 'description', 'category', 'amount', 'is_anomaly']
