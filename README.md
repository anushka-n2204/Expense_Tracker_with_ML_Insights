# 💰 Smart Expense Tracker with ML Insights

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A personal finance web application that uses machine learning to automatically categorize expenses, detect spending anomalies, and provide intelligent insights.



> Built as an academic project for B.Tech CSE – AI & ML Specialisation at SRM Institute of Science and Technology, KTR

## 🎯 Features

- **Expense Management**: Add, edit, delete, and view expenses with an intuitive interface
- **ML Auto-Categorization**: Automatically predicts expense categories using NLP (TF-IDF + Logistic Regression)
- **Anomaly Detection**: Flags unusual spending patterns using Isolation Forest algorithm
- **Visual Dashboards**: Interactive charts showing spending trends and patterns
- **Budget Management**: Set monthly budgets with alerts at 80% and 100% thresholds
- **Data Export**: Export expenses to CSV format
- **Lightweight**: Runs on low-resource hardware (i3, 4GB RAM)

## 📋 Requirements

- Python 3.9 or higher
- 4GB RAM minimum
- Windows, macOS, or Linux

## 🚀 Installation

### Option 1: Clone from GitHub

```bash
git clone https://github.com/anushka-n2204/smart-expense-tracker.git
cd smart-expense-tracker
```

### Option 2: Download ZIP

Download the repository as ZIP and extract it.

### Install Dependencies
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
expense-tracker/
├── app.py              # Main Streamlit application
├── model.py            # ML categorization model
├── anomaly.py          # Anomaly detection logic
├── database.py         # SQLite database operations
├── utils.py            # Helper functions
├── requirements.txt    # Python dependencies
├── data/
│   ├── expenses.db     # SQLite database (auto-created)
│   └── training_data.csv  # Training data for ML model
└── models/
    └── categorizer.pkl # Saved trained model (auto-created)
```

## 🎓 Usage Guide

### 1. Train the ML Model (First Time Setup)

1. Navigate to **"Train Model"** page
2. The app includes 300+ sample training records
3. Click **"Train Model"** button
4. Wait for training to complete (should achieve >85% accuracy)

### 2. Add Expenses

1. Go to **"Add Expense"** page
2. Enter date, amount, and description
3. The ML model will auto-predict the category
4. You can override the prediction if needed
5. Click **"Add Expense"**

### 3. View Dashboard

The dashboard shows:
- Total spending for current month
- Budget usage with progress bar
- Spending by category (pie chart)
- Daily spending trend (line chart)
- Monthly spending over last 6 months (bar chart)
- Top 3 spending categories

### 4. Manage Expenses

1. Go to **"View Expenses"** page
2. Filter by category, date range, or flagged expenses
3. Export data to CSV
4. Delete expenses by ID

### 5. Configure Settings

1. Go to **"Settings"** page
2. Set your monthly budget
3. Re-run anomaly detection if needed
4. View database statistics

## 🤖 ML Models

### Categorization Model
- **Algorithm**: TF-IDF Vectorization + Logistic Regression
- **Categories**: Food, Transport, Shopping, Utilities, Health, Entertainment, Education, Other
- **Target Accuracy**: >85% on test split
- **Training Time**: <10 seconds on CPU
- **Model Size**: <1 MB

### Anomaly Detection
- **Algorithm**: Isolation Forest + Statistical Analysis
- **Method**: Detects expenses >2 standard deviations above category mean
- **Data Window**: Last 90 days
- **Contamination**: 5% (adjustable)

## 📊 Categories

The system supports 8 expense categories:

1. **Food**: Restaurants, groceries, food delivery
2. **Transport**: Uber, Ola, metro, fuel, parking
3. **Shopping**: Online shopping, clothing, electronics
4. **Utilities**: Electricity, water, internet, mobile bills
5. **Health**: Medicine, doctor visits, gym, insurance
6. **Entertainment**: Netflix, movies, concerts, subscriptions
7. **Education**: Courses, books, certifications, tuition
8. **Other**: Everything else

## 🔧 Customization

### Add More Training Data

Edit `data/training_data.csv` and add rows with:
- `description`: Expense description text
- `category`: One of the 8 categories

Then retrain the model from the "Train Model" page.

### Adjust Anomaly Sensitivity

In `anomaly.py`, modify the `contamination` parameter (default: 0.05 = 5%)

### Change Budget

Use the Settings page to update your monthly budget.

## 📈 Performance

- **App Load Time**: <3 seconds on i3/4GB RAM
- **ML Prediction**: <500ms per prediction
- **Database**: SQLite (file-based, no server needed)
- **Disk Usage**: <100MB total

## 🎓 Academic Project

**Institution**: SRM Institute of Science and Technology, KTR  
**Program**: B.Tech CSE – AI & ML Specialisation  
**Version**: 1.0  
**Date**: May 2026

## 📝 License

This is an academic project for educational purposes.

## 🤝 Contributing

This is a student project. For suggestions or improvements, please contact the project owner.

## 📧 Support

For issues or questions, please refer to the project documentation or contact your academic supervisor.

---

**Built with ❤️ using Streamlit, Scikit-learn, and Python**
