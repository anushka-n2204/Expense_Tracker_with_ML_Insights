# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd expense-tracker
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Step 3: Train the ML Model

1. Click on **"Train Model"** in the sidebar
2. Click the **"Train Model"** button
3. Wait ~5-10 seconds for training to complete
4. You should see accuracy >85%

## ✅ You're Ready!

Now you can:
- Add expenses (they'll be auto-categorized!)
- View your dashboard with charts
- Set a monthly budget
- Export data to CSV

## 🎯 First Time Tips

1. **Add some expenses first** - The dashboard looks better with data!
2. **Set your budget** - Go to Settings and set a realistic monthly budget
3. **Check predictions** - When adding expenses, see how accurate the ML predictions are
4. **View anomalies** - After adding 10+ expenses, unusual ones will be flagged

## 🐛 Troubleshooting

**App won't start?**
- Make sure Python 3.9+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**Model training fails?**
- Check that `data/training_data.csv` exists
- Make sure it has 'description' and 'category' columns

**Database errors?**
- The database is auto-created on first run
- Check that the `data/` folder exists

## 📱 Using the App

### Dashboard
- View all your spending statistics
- See charts and trends
- Monitor budget usage

### Add Expense
- Enter amount and description
- ML auto-predicts category
- Override if needed

### View Expenses
- Filter by date or category
- Export to CSV
- Delete expenses

### Train Model
- Retrain with new data
- View accuracy metrics
- Check classification report

### Settings
- Set monthly budget
- Re-run anomaly detection
- View database stats

## 🎓 Sample Data

The app comes with 300+ training samples covering:
- Food (restaurants, groceries, delivery)
- Transport (Uber, Ola, metro, fuel)
- Shopping (Amazon, Flipkart, clothing)
- Utilities (bills, recharge, maintenance)
- Health (medicine, doctor, gym)
- Entertainment (Netflix, movies, concerts)
- Education (courses, books, certifications)
- Other (miscellaneous expenses)

## 💡 Pro Tips

1. **Be descriptive** - Better descriptions = better predictions
   - Good: "Swiggy chicken biryani order"
   - Bad: "Food"

2. **Review predictions** - The model learns from patterns in training data

3. **Check anomalies** - Flagged expenses might be data entry errors

4. **Export regularly** - Keep CSV backups of your data

5. **Retrain periodically** - Add more training data and retrain for better accuracy

## 🎉 Enjoy Tracking Your Expenses!

Built with Streamlit, Scikit-learn, and Python 🐍
