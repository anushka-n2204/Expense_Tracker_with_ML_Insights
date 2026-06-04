# Installation & Usage Guide

## 📦 Complete Installation Instructions

### Prerequisites

Before you begin, ensure you have:
- **Python 3.9 or higher** installed on your system
- **pip** (Python package manager) installed
- **4GB RAM** minimum
- **100MB free disk space**

### Step-by-Step Installation

#### 1. Verify Python Installation

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
python --version
```

You should see Python 3.9.x or higher. If not, download from [python.org](https://www.python.org/downloads/)

#### 2. Navigate to Project Directory

```bash
cd expense-tracker
```

#### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (1.32.0) - Web framework
- pandas (2.2.0) - Data processing
- scikit-learn (1.4.0) - Machine learning
- plotly (5.18.0) - Interactive charts

**Installation time**: ~2-3 minutes depending on internet speed

#### 4. Verify Installation

Run the test script to ensure everything is set up correctly:

```bash
python test_setup.py
```

You should see all green checkmarks (✅). If you see any red crosses (❌), follow the error messages to fix issues.

#### 5. Launch the Application

```bash
streamlit run app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

**First launch may take 10-15 seconds as Streamlit initializes.**

## 🎯 First-Time Setup

### Train the ML Model (Required)

1. In the app, click **"Train Model"** in the left sidebar
2. You'll see the training data (300+ samples)
3. Click the **"🚀 Train Model"** button
4. Wait 5-10 seconds for training to complete
5. Check that accuracy is **>85%** (usually 87-92%)

**You only need to do this once!** The trained model is saved and will be loaded automatically on future runs.

## 📱 Using the Application

### Page 1: Dashboard 📊

**What you'll see:**
- Total spending for current month
- Number of expenses
- Budget remaining
- Flagged (anomalous) expenses
- Budget usage progress bar
- Pie chart of spending by category
- Daily spending line chart
- Monthly spending bar chart (last 6 months)
- Top 3 spending categories

**When to use:** Check your financial overview anytime

### Page 2: Add Expense ➕

**How to add an expense:**
1. Select the date (defaults to today)
2. Enter the amount in rupees
3. Type a description (e.g., "Swiggy chicken biryani order")
4. Watch the ML model auto-predict the category!
5. Override the category if needed
6. Click "Add Expense"

**ML Magic:** As you type the description, the model predicts the category in real-time. You'll also see confidence scores for all categories.

**Anomaly Detection:** If your expense is unusually high for that category, you'll see a warning.

### Page 3: View Expenses 📋

**Features:**
- **Filter by Category**: Select specific category or "All"
- **Filter by Date**: This Month, Last 30 Days, Last 90 Days, or All Time
- **Show Only Flagged**: See only anomalous expenses
- **Export to CSV**: Download all expenses
- **Delete Expense**: Remove by ID

**Table shows:** ID, Date, Description, Category, Amount, Flagged status

### Page 4: Train Model 🤖

**When to use:**
- First time setup (required)
- After adding more training data
- To retrain with updated samples

**What you'll see:**
- Training data preview
- Number of samples
- Train button
- Accuracy metrics after training
- Classification report (precision, recall, F1-score)

**Expected Results:**
- Accuracy: 85-92%
- Training time: 5-10 seconds
- Model size: <1 MB

### Page 5: Settings ⚙️

**Configure:**

1. **Monthly Budget**
   - Set your spending limit
   - Default: ₹10,000
   - Adjust based on your needs

2. **Refresh Anomaly Detection**
   - Re-run detection on all expenses
   - Use after adding many expenses
   - Updates flagged status

3. **Database Statistics**
   - Total expenses count
   - Total amount spent
   - Date range of data

4. **Model Status**
   - Check if ML model is trained
   - See model readiness

## 🎓 Sample Workflow

### Day 1: Setup
```
1. Install dependencies
2. Run test_setup.py
3. Launch app
4. Train ML model
5. Set monthly budget (₹15,000)
```

### Day 2: Add Expenses
```
1. Add breakfast: "Cafe coffee and sandwich" → Auto-categorized as Food
2. Add transport: "Uber to office" → Auto-categorized as Transport
3. Add shopping: "Amazon headphones" → Auto-categorized as Shopping
4. Check dashboard to see charts
```

### Week 1: Regular Use
```
1. Add expenses daily
2. Check dashboard weekly
3. Review flagged expenses
4. Monitor budget usage
```

### Month End: Analysis
```
1. View all expenses
2. Export to CSV for records
3. Check spending by category
4. Set next month's budget
```

## 🐛 Troubleshooting

### Issue: "streamlit: command not found"

**Solution:**
```bash
pip install --upgrade streamlit
# or
python -m streamlit run app.py
```

### Issue: "ModuleNotFoundError: No module named 'sklearn'"

**Solution:**
```bash
pip install scikit-learn
```

### Issue: "Database is locked"

**Solution:**
- Close any other instances of the app
- Delete `data/expenses.db` and restart (will lose data)

### Issue: "Model not trained" warning

**Solution:**
- Go to "Train Model" page
- Click "Train Model" button
- Wait for completion

### Issue: Charts not displaying

**Solution:**
- Ensure plotly is installed: `pip install plotly`
- Clear browser cache
- Try a different browser

### Issue: App is slow

**Solution:**
- Close other applications
- Reduce number of expenses displayed (use filters)
- Check if running on low-spec hardware

## 💡 Tips for Best Results

### For Accurate Predictions

1. **Be descriptive**: "Swiggy biryani order" is better than "food"
2. **Include brand names**: "Uber ride" vs "cab"
3. **Be consistent**: Use similar descriptions for similar expenses

### For Better Anomaly Detection

1. **Add at least 10 expenses** before expecting accurate anomaly detection
2. **Add expenses regularly** for 2-3 weeks to establish patterns
3. **Review flagged expenses** - they might be legitimate large purchases

### For Useful Insights

1. **Add expenses daily** rather than in bulk
2. **Use correct dates** for accurate trends
3. **Set realistic budgets** based on past spending
4. **Export data monthly** for backup

## 🔒 Data Privacy

- **All data is stored locally** on your computer
- **No internet connection required** after installation
- **No data is sent to external servers**
- **Database file**: `data/expenses.db`
- **Backup**: Export to CSV regularly

## 📊 Understanding the ML Model

### How Auto-Categorization Works

1. **Training**: Model learns from 300+ labeled examples
2. **Feature Extraction**: Converts text to numerical features (TF-IDF)
3. **Classification**: Logistic Regression predicts category
4. **Confidence**: Shows probability for each category

### Categories Explained

- **Food**: Restaurants, groceries, food delivery, cafes
- **Transport**: Uber, Ola, metro, fuel, parking, tolls
- **Shopping**: Online shopping, clothing, electronics, accessories
- **Utilities**: Bills (electricity, water, internet), recharges
- **Health**: Medicine, doctor visits, gym, insurance
- **Entertainment**: Netflix, movies, concerts, subscriptions
- **Education**: Courses, books, certifications, tuition
- **Other**: Everything else (donations, gifts, miscellaneous)

### How Anomaly Detection Works

1. **Statistical Analysis**: Calculates mean and standard deviation per category
2. **Threshold**: Flags expenses >2 standard deviations above mean
3. **Isolation Forest**: ML algorithm for outlier detection
4. **Visual Flag**: Shows ⚠️ in expense table

## 🎯 Performance Expectations

### On Recommended Hardware (i5, 8GB RAM)
- App load: 2-3 seconds
- Page navigation: Instant
- ML prediction: <100ms
- Chart rendering: <1 second
- Model training: 5-7 seconds

### On Minimum Hardware (i3, 4GB RAM)
- App load: 3-5 seconds
- Page navigation: <1 second
- ML prediction: <500ms
- Chart rendering: 1-2 seconds
- Model training: 8-10 seconds

## 📞 Getting Help

### Check These First
1. Run `python test_setup.py` to diagnose issues
2. Check that all files are present (see README.md)
3. Verify Python version: `python --version`
4. Reinstall dependencies: `pip install -r requirements.txt`

### Common Questions

**Q: Can I use this on multiple computers?**  
A: Yes, but you'll need to copy the entire folder including the `data/` directory to transfer your expenses.

**Q: Can multiple people use this?**  
A: Currently it's single-user. Each person should have their own installation.

**Q: How do I backup my data?**  
A: Export to CSV regularly, or copy the `data/expenses.db` file.

**Q: Can I add my own categories?**  
A: Yes, but you'll need to modify the code in `model.py` and retrain with new training data.

**Q: Does this work offline?**  
A: Yes! After installation, no internet connection is needed.

## 🎉 You're All Set!

Enjoy tracking your expenses with ML-powered insights!

---

**Need more help?** Check:
- README.md - Complete documentation
- QUICKSTART.md - Quick 3-step guide
- PROJECT_SUMMARY.md - Technical details
- test_setup.py - Diagnostic tool
