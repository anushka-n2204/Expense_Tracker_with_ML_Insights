"""
Smart Expense Tracker with ML Insights
Main Streamlit application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

from database import Database
from model import ExpenseCategorizer
from anomaly import AnomalyDetector
from utils import (
    get_current_month_range, 
    format_currency, 
    export_to_csv,
    calculate_budget_percentage
)

# Page configuration
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Smart Expense Tracker with ML Insights v1.0 - Built for SRM Institute"
    }
)

# Initialize components
@st.cache_resource
def init_components():
    """Initialize database and ML models"""
    db = Database()
    categorizer = ExpenseCategorizer()
    detector = AnomalyDetector()
    return db, categorizer, detector

db, categorizer, detector = init_components()

# Sidebar navigation
st.sidebar.title("💰 Expense Tracker")

# Show welcome message if model not trained
if st.session_state.show_welcome:
    st.sidebar.warning("⚠️ First time? Train the model first!")

page = st.sidebar.radio("Navigate", ["Dashboard", "Add Expense", "View Expenses", "Train Model", "Settings"])

# Quick stats in sidebar
all_expenses = db.get_all_expenses()
if not all_expenses.empty:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Total Expenses", len(all_expenses))
    st.sidebar.metric("Total Spent", format_currency(all_expenses['amount'].sum()))
    
    # Model status
    if categorizer.is_trained():
        st.sidebar.success("✅ ML Model Ready")
    else:
        st.sidebar.error("❌ Model Not Trained")

# Initialize session state
if 'monthly_budget' not in st.session_state:
    st.session_state.monthly_budget = 10000.0

if 'show_welcome' not in st.session_state:
    # Check if model is trained
    if not categorizer.is_trained():
        st.session_state.show_welcome = True
    else:
        st.session_state.show_welcome = False


# ===== DASHBOARD PAGE =====
if page == "Dashboard":
    st.title("📊 Dashboard")
    
    # Get current month data
    start_date, end_date = get_current_month_range()
    current_month_df = db.get_expenses_by_date_range(start_date, end_date)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spent = current_month_df['amount'].sum() if not current_month_df.empty else 0
        st.metric("Total Spending (This Month)", format_currency(total_spent))
    
    with col2:
        num_expenses = len(current_month_df)
        st.metric("Number of Expenses", num_expenses)
    
    with col3:
        budget = st.session_state.monthly_budget
        remaining = budget - total_spent
        st.metric("Budget Remaining", format_currency(remaining))
    
    with col4:
        anomalies = current_month_df[current_month_df['is_anomaly'] == 1]
        st.metric("Flagged Expenses", len(anomalies))
    
    # Budget progress bar
    st.subheader("💳 Budget Usage")
    budget_pct = calculate_budget_percentage(total_spent, st.session_state.monthly_budget)
    
    if budget_pct >= 100:
        st.error(f"⚠️ Budget exceeded! You've spent {budget_pct:.1f}% of your monthly budget.")
    elif budget_pct >= 80:
        st.warning(f"⚠️ Warning: You've used {budget_pct:.1f}% of your monthly budget.")
    else:
        st.info(f"You've used {budget_pct:.1f}% of your monthly budget.")
    
    st.progress(min(budget_pct / 100, 1.0))
    
    # Visualizations
    if not current_month_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart - spending by category
            st.subheader("📈 Spending by Category")
            category_totals = current_month_df.groupby('category')['amount'].sum().reset_index()
            fig_pie = px.pie(category_totals, values='amount', names='category', 
                            title='Current Month Category Breakdown',
                            hole=0.4)  # Donut chart
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Top 3 categories
            st.subheader("🔝 Top 3 Spending Categories")
            top_3 = category_totals.nlargest(3, 'amount')
            for idx, row in top_3.iterrows():
                pct = (row['amount'] / category_totals['amount'].sum()) * 100
                st.write(f"**{row['category']}**: {format_currency(row['amount'])} ({pct:.1f}%)")
        
        with col2:
            # Line chart - daily spending
            st.subheader("📉 Daily Spending Trend")
            daily_spending = current_month_df.groupby('date')['amount'].sum().reset_index()
            daily_spending['date'] = pd.to_datetime(daily_spending['date'])
            
            # Add average line
            avg_daily = daily_spending['amount'].mean()
            fig_line = px.line(daily_spending, x='date', y='amount', 
                              title='Daily Spending (Current Month)')
            fig_line.add_hline(y=avg_daily, line_dash="dash", line_color="red",
                              annotation_text=f"Avg: {format_currency(avg_daily)}")
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Spending Insights
        st.subheader("💡 Smart Insights")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_expense = current_month_df['amount'].mean()
            st.metric("Average Expense", format_currency(avg_expense))
        
        with col2:
            largest_expense = current_month_df['amount'].max()
            st.metric("Largest Expense", format_currency(largest_expense))
        
        with col3:
            days_left = (pd.to_datetime(end_date) - datetime.now()).days
            if days_left > 0 and budget > total_spent:
                daily_budget = (budget - total_spent) / days_left
                st.metric("Daily Budget Left", format_currency(daily_budget))
            else:
                st.metric("Days in Month", days_left if days_left > 0 else 0)
        
        # Bar chart - monthly spending (last 6 months)
        st.subheader("📊 Monthly Spending Trend")
        monthly_totals = db.get_monthly_totals(months=6)
        if not monthly_totals.empty:
            fig_bar = px.bar(monthly_totals, x='month', y='total', 
                            title='Last 6 Months Spending',
                            labels={'month': 'Month', 'total': 'Amount (₹)'},
                            text='total')
            fig_bar.update_traces(texttemplate='₹%{text:.0f}', textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No expenses recorded for this month yet. Add your first expense!")


# ===== ADD EXPENSE PAGE =====
elif page == "Add Expense":
    st.title("➕ Add New Expense")
    
    with st.form("add_expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            expense_date = st.date_input("Date", value=datetime.now())
            expense_amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        
        with col2:
            expense_description = st.text_input("Description", placeholder="e.g., Lunch at restaurant")
            
            # Auto-predict category if model is trained
            predicted_category = "Other"
            if expense_description and categorizer.is_trained():
                predicted_category = categorizer.predict(expense_description)
            
            expense_category = st.selectbox(
                "Category",
                options=categorizer.categories,
                index=categorizer.categories.index(predicted_category) if predicted_category in categorizer.categories else 0
            )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("Add Expense", use_container_width=True)
        with col2:
            clear = st.form_submit_button("Clear", use_container_width=True)
        
        if submitted:
            if expense_amount <= 0:
                st.error("Amount must be greater than 0")
            elif not expense_description:
                st.error("Description is required")
            else:
                # Add expense to database
                expense_id = db.add_expense(
                    date=expense_date.strftime('%Y-%m-%d'),
                    description=expense_description,
                    category=expense_category,
                    amount=expense_amount
                )
                
                st.success(f"✅ Expense added successfully! (ID: {expense_id})")
                
                # Check for anomalies
                recent_expenses = db.get_expenses_last_n_days(90)
                if len(recent_expenses) >= 10:
                    anomaly_ids = detector.detect_category_anomalies(recent_expenses)
                    if expense_id in anomaly_ids:
                        db.update_anomaly_flag(expense_id, 1)
                        st.warning("⚠️ This expense has been flagged as unusual for this category.")
    
    # Show prediction confidence if model is trained
    if expense_description and categorizer.is_trained():
        st.subheader("🤖 ML Prediction Confidence")
        probabilities = categorizer.predict_proba(expense_description)
        prob_df = pd.DataFrame(list(probabilities.items()), columns=['Category', 'Confidence'])
        prob_df = prob_df.sort_values('Confidence', ascending=False)
        prob_df['Confidence'] = prob_df['Confidence'].apply(lambda x: f"{x*100:.1f}%")
        st.dataframe(prob_df, hide_index=True)
    
    # Quick Add - Recent Expenses
    st.subheader("⚡ Quick Add from Recent")
    recent_expenses = db.get_all_expenses().head(5)
    if not recent_expenses.empty:
        st.write("Click to add similar expense:")
        for idx, row in recent_expenses.iterrows():
            if st.button(f"💰 {row['description']} - {format_currency(row['amount'])} ({row['category']})", key=f"quick_{row['id']}"):
                st.session_state['quick_description'] = row['description']
                st.session_state['quick_amount'] = row['amount']
                st.session_state['quick_category'] = row['category']
                st.info(f"✅ Pre-filled with: {row['description']}")


# ===== VIEW EXPENSES PAGE =====
elif page == "View Expenses":
    st.title("📋 View & Manage Expenses")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + categorizer.categories)
    
    with col2:
        date_range = st.selectbox("Date Range", ["All Time", "This Month", "Last 30 Days", "Last 90 Days", "Custom"])
    
    with col3:
        show_anomalies = st.checkbox("Show Only Flagged Expenses")
    
    # Custom date range
    if date_range == "Custom":
        col1, col2 = st.columns(2)
        with col1:
            custom_start = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
        with col2:
            custom_end = st.date_input("End Date", value=datetime.now())
    
    # Search box
    search_query = st.text_input("🔍 Search by description", placeholder="e.g., Swiggy, Uber, Netflix")
    
    # Get expenses based on filters
    if date_range == "This Month":
        start_date, end_date = get_current_month_range()
        expenses_df = db.get_expenses_by_date_range(start_date, end_date)
    elif date_range == "Last 30 Days":
        expenses_df = db.get_expenses_last_n_days(30)
    elif date_range == "Last 90 Days":
        expenses_df = db.get_expenses_last_n_days(90)
    elif date_range == "Custom":
        expenses_df = db.get_expenses_by_date_range(
            custom_start.strftime('%Y-%m-%d'), 
            custom_end.strftime('%Y-%m-%d')
        )
    else:
        expenses_df = db.get_all_expenses()
    
    # Apply category filter
    if filter_category != "All":
        expenses_df = expenses_df[expenses_df['category'] == filter_category]
    
    # Apply search filter
    if search_query:
        expenses_df = expenses_df[expenses_df['description'].str.contains(search_query, case=False, na=False)]
    
    # Apply anomaly filter
    if show_anomalies:
        expenses_df = expenses_df[expenses_df['is_anomaly'] == 1]
    
    # Display expenses
    if not expenses_df.empty:
        st.write(f"**Total Expenses:** {len(expenses_df)} | **Total Amount:** {format_currency(expenses_df['amount'].sum())}")
        
        # Format display
        display_df = expenses_df[['id', 'date', 'description', 'category', 'amount', 'is_anomaly']].copy()
        display_df['amount'] = display_df['amount'].apply(format_currency)
        display_df['is_anomaly'] = display_df['is_anomaly'].apply(lambda x: '⚠️ Yes' if x == 1 else 'No')
        display_df.columns = ['ID', 'Date', 'Description', 'Category', 'Amount', 'Flagged']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export to CSV
        if st.button("📥 Export to CSV"):
            filename = export_to_csv(expenses_df)
            st.success(f"Exported to {filename}")
            with open(filename, 'rb') as f:
                st.download_button("Download CSV", f, file_name=filename)
        
        # Edit expense
        st.subheader("✏️ Edit Expense")
        with st.expander("Click to edit an expense"):
            edit_id = st.number_input("Enter Expense ID to edit", min_value=1, step=1, key="edit_id")
            
            if edit_id and not expenses_df.empty and edit_id in expenses_df['id'].values:
                expense_to_edit = expenses_df[expenses_df['id'] == edit_id].iloc[0]
                
                with st.form("edit_expense_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_date = st.date_input("Date", value=pd.to_datetime(expense_to_edit['date']))
                        edit_amount = st.number_input("Amount (₹)", value=float(expense_to_edit['amount']), min_value=0.0, step=10.0)
                    
                    with col2:
                        edit_description = st.text_input("Description", value=expense_to_edit['description'])
                        edit_category = st.selectbox("Category", options=categorizer.categories, 
                                                    index=categorizer.categories.index(expense_to_edit['category']))
                    
                    if st.form_submit_button("Update Expense"):
                        db.update_expense(edit_id, edit_date.strftime('%Y-%m-%d'), 
                                        edit_description, edit_category, edit_amount)
                        st.success(f"✅ Expense {edit_id} updated successfully!")
                        st.rerun()
        
        # Delete expense
        st.subheader("🗑️ Delete Expense")
        with st.expander("Click to delete an expense"):
            delete_id = st.number_input("Enter Expense ID to delete", min_value=1, step=1, key="delete_id")
            if st.button("Delete", type="primary"):
                try:
                    db.delete_expense(delete_id)
                    st.success(f"Expense {delete_id} deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting expense: {e}")
    else:
        st.info("No expenses found matching the filters.")


# ===== TRAIN MODEL PAGE =====
elif page == "Train Model":
    st.title("🤖 Train ML Model")
    
    st.write("""
    Train the expense categorization model using your training data.
    The model uses TF-IDF vectorization with Logistic Regression.
    """)
    
    training_file = "data/training_data.csv"
    
    if os.path.exists(training_file):
        st.success(f"✅ Training data found: {training_file}")
        
        # Show sample data
        training_df = pd.read_csv(training_file)
        st.write(f"**Total training samples:** {len(training_df)}")
        st.write("**Sample data:**")
        st.dataframe(training_df.head(10))
        
        if st.button("🚀 Train Model"):
            with st.spinner("Training model..."):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Loading training data...")
                    progress_bar.progress(20)
                    
                    status_text.text("Training TF-IDF vectorizer...")
                    progress_bar.progress(40)
                    
                    accuracy, report = categorizer.train(training_file)
                    
                    status_text.text("Evaluating model...")
                    progress_bar.progress(80)
                    
                    status_text.text("Saving model...")
                    progress_bar.progress(100)
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.success(f"✅ Model trained successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Test Accuracy", f"{accuracy*100:.2f}%")
                    with col2:
                        st.metric("Training Samples", len(training_df))
                    with col3:
                        st.metric("Categories", len(categorizer.categories))
                    
                    # Show classification report
                    st.subheader("📊 Classification Report")
                    report_df = pd.DataFrame(report).transpose()
                    st.dataframe(report_df.style.format("{:.2f}"))
                    
                    if accuracy >= 0.85:
                        st.balloons()
                        st.success("🎉 Model meets the target accuracy of >85%!")
                    else:
                        st.warning("⚠️ Model accuracy is below target. Consider adding more training data.")
                        
                except Exception as e:
                    st.error(f"Error training model: {e}")
    else:
        st.warning(f"⚠️ Training data not found at {training_file}")
        st.info("Please create a CSV file with 'description' and 'category' columns.")
        
        # Option to create sample training data
        if st.button("Generate Sample Training Data"):
            sample_data = {
                'description': [
                    'Swiggy order chicken biryani', 'Zomato pizza delivery', 'Restaurant dinner',
                    'Uber ride to airport', 'Ola cab to office', 'Metro card recharge',
                    'Amazon laptop stand', 'Flipkart shoes', 'Online shopping clothes',
                    'Electricity bill payment', 'Water bill', 'Internet broadband',
                    'Apollo pharmacy medicine', 'Doctor consultation', 'Medical tests',
                    'Netflix subscription', 'Movie tickets', 'Concert tickets',
                    'Udemy course Python', 'Book purchase', 'Online certification'
                ] * 15,  # Repeat to get ~300 rows
                'category': [
                    'Food', 'Food', 'Food',
                    'Transport', 'Transport', 'Transport',
                    'Shopping', 'Shopping', 'Shopping',
                    'Utilities', 'Utilities', 'Utilities',
                    'Health', 'Health', 'Health',
                    'Entertainment', 'Entertainment', 'Entertainment',
                    'Education', 'Education', 'Education'
                ] * 15
            }
            sample_df = pd.DataFrame(sample_data)
            sample_df.to_csv(training_file, index=False)
            st.success(f"✅ Sample training data created at {training_file}")
            st.rerun()


# ===== SETTINGS PAGE =====
elif page == "Settings":
    st.title("⚙️ Settings")
    
    st.subheader("💰 Monthly Budget")
    new_budget = st.number_input(
        "Set Monthly Budget (₹)", 
        min_value=0.0, 
        value=st.session_state.monthly_budget,
        step=1000.0
    )
    
    if st.button("Save Budget"):
        st.session_state.monthly_budget = new_budget
        st.success("Budget updated successfully!")
    
    # Category-wise budgets
    st.subheader("📊 Category-wise Budgets (Optional)")
    with st.expander("Set budgets for specific categories"):
        if 'category_budgets' not in st.session_state:
            st.session_state.category_budgets = {}
        
        for category in categorizer.categories:
            current_budget = st.session_state.category_budgets.get(category, 0.0)
            new_cat_budget = st.number_input(
                f"{category} Budget (₹)", 
                min_value=0.0, 
                value=current_budget,
                step=500.0,
                key=f"budget_{category}"
            )
            st.session_state.category_budgets[category] = new_cat_budget
        
        # Show category spending vs budget
        st.write("**Current Month Category Spending:**")
        start_date, end_date = get_current_month_range()
        category_spending = db.get_category_totals(start_date, end_date)
        
        for idx, row in category_spending.iterrows():
            cat = row['category']
            spent = row['total']
            budget_cat = st.session_state.category_budgets.get(cat, 0)
            
            if budget_cat > 0:
                pct = (spent / budget_cat) * 100
                if pct >= 100:
                    st.error(f"{cat}: {format_currency(spent)} / {format_currency(budget_cat)} ({pct:.0f}%)")
                elif pct >= 80:
                    st.warning(f"{cat}: {format_currency(spent)} / {format_currency(budget_cat)} ({pct:.0f}%)")
                else:
                    st.success(f"{cat}: {format_currency(spent)} / {format_currency(budget_cat)} ({pct:.0f}%)")
    
    st.subheader("🔄 Refresh Anomaly Detection")
    if st.button("Re-run Anomaly Detection"):
        with st.spinner("Detecting anomalies..."):
            # Reset all anomaly flags
            all_expenses = db.get_all_expenses()
            for expense_id in all_expenses['id']:
                db.update_anomaly_flag(expense_id, 0)
            
            # Run anomaly detection on last 90 days
            recent_expenses = db.get_expenses_last_n_days(90)
            if len(recent_expenses) >= 10:
                anomaly_ids = detector.detect_category_anomalies(recent_expenses)
                for expense_id in anomaly_ids:
                    db.update_anomaly_flag(expense_id, 1)
                st.success(f"✅ Anomaly detection complete! Flagged {len(anomaly_ids)} expenses.")
            else:
                st.info("Not enough data for anomaly detection (minimum 10 expenses required).")
    
    st.subheader("📊 Database Statistics")
    all_expenses = db.get_all_expenses()
    st.write(f"**Total Expenses:** {len(all_expenses)}")
    st.write(f"**Total Amount:** {format_currency(all_expenses['amount'].sum() if not all_expenses.empty else 0)}")
    st.write(f"**Date Range:** {all_expenses['date'].min() if not all_expenses.empty else 'N/A'} to {all_expenses['date'].max() if not all_expenses.empty else 'N/A'}")
    
    st.subheader("💾 Data Backup & Import")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Backup Database**")
        if st.button("📥 Download Backup (CSV)"):
            if not all_expenses.empty:
                filename = f"expense_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                backup_file = export_to_csv(all_expenses, filename)
                with open(backup_file, 'rb') as f:
                    st.download_button(
                        "⬇️ Download Backup File",
                        f,
                        file_name=filename,
                        mime="text/csv"
                    )
            else:
                st.info("No data to backup")
    
    with col2:
        st.write("**Import Data**")
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file is not None:
            try:
                import_df = pd.read_csv(uploaded_file)
                required_cols = ['date', 'description', 'category', 'amount']
                
                if all(col in import_df.columns for col in required_cols):
                    if st.button("Import Data"):
                        count = 0
                        for _, row in import_df.iterrows():
                            db.add_expense(
                                date=row['date'],
                                description=row['description'],
                                category=row['category'],
                                amount=float(row['amount']),
                                is_anomaly=int(row.get('is_anomaly', 0))
                            )
                            count += 1
                        st.success(f"✅ Imported {count} expenses!")
                        st.rerun()
                else:
                    st.error(f"CSV must have columns: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"Error importing: {e}")
    
    st.subheader("🤖 Model Status")
    if categorizer.is_trained():
        st.success("✅ ML Model is trained and ready")
    else:
        st.warning("⚠️ ML Model not trained. Go to 'Train Model' page.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**Smart Expense Tracker v1.0**  
Built with Streamlit & ML  
SRM Institute of Science and Technology
""")
