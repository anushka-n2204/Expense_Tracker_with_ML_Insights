"""
Test script to verify the expense tracker setup
Run this before starting the app to ensure everything works
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not found. Run: pip install streamlit")
        return False
    
    try:
        import pandas
        print("✅ Pandas installed")
    except ImportError:
        print("❌ Pandas not found. Run: pip install pandas")
        return False
    
    try:
        import sklearn
        print("✅ Scikit-learn installed")
    except ImportError:
        print("❌ Scikit-learn not found. Run: pip install scikit-learn")
        return False
    
    try:
        import plotly
        print("✅ Plotly installed")
    except ImportError:
        print("❌ Plotly not found. Run: pip install plotly")
        return False
    
    return True

def test_modules():
    """Test if all project modules can be imported"""
    print("\nTesting project modules...")
    try:
        from database import Database
        print("✅ database.py working")
    except Exception as e:
        print(f"❌ database.py error: {e}")
        return False
    
    try:
        from model import ExpenseCategorizer
        print("✅ model.py working")
    except Exception as e:
        print(f"❌ model.py error: {e}")
        return False
    
    try:
        from anomaly import AnomalyDetector
        print("✅ anomaly.py working")
    except Exception as e:
        print(f"❌ anomaly.py error: {e}")
        return False
    
    try:
        from utils import format_currency, get_current_month_range
        print("✅ utils.py working")
    except Exception as e:
        print(f"❌ utils.py error: {e}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directory structure...")
    
    if not os.path.exists("data"):
        print("❌ data/ directory not found")
        return False
    print("✅ data/ directory exists")
    
    if not os.path.exists("models"):
        print("❌ models/ directory not found")
        return False
    print("✅ models/ directory exists")
    
    if not os.path.exists("data/training_data.csv"):
        print("❌ training_data.csv not found")
        return False
    print("✅ training_data.csv exists")
    
    return True

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    try:
        from database import Database
        db = Database()
        print("✅ Database initialized successfully")
        
        # Test adding and retrieving
        test_id = db.add_expense(
            date="2026-05-31",
            description="Test expense",
            category="Other",
            amount=100.0
        )
        print(f"✅ Test expense added (ID: {test_id})")
        
        # Retrieve and verify
        expenses = db.get_all_expenses()
        if len(expenses) > 0:
            print(f"✅ Database query working ({len(expenses)} expenses)")
        
        # Clean up test expense
        db.delete_expense(test_id)
        print("✅ Test expense deleted")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_model():
    """Test ML model"""
    print("\nTesting ML model...")
    try:
        from model import ExpenseCategorizer
        categorizer = ExpenseCategorizer()
        print("✅ Categorizer initialized")
        
        # Test prediction (will return "Other" if not trained)
        prediction = categorizer.predict("Swiggy food order")
        print(f"✅ Prediction working (predicted: {prediction})")
        
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_training_data():
    """Test training data format"""
    print("\nTesting training data...")
    try:
        import pandas as pd
        df = pd.read_csv("data/training_data.csv")
        
        if 'description' not in df.columns:
            print("❌ 'description' column missing in training data")
            return False
        
        if 'category' not in df.columns:
            print("❌ 'category' column missing in training data")
            return False
        
        print(f"✅ Training data format correct ({len(df)} samples)")
        
        # Check categories
        categories = df['category'].unique()
        print(f"✅ Categories found: {', '.join(categories)}")
        
        return True
    except Exception as e:
        print(f"❌ Training data error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Smart Expense Tracker - Setup Verification")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_directories()
    all_passed &= test_modules()
    all_passed &= test_training_data()
    all_passed &= test_database()
    all_passed &= test_model()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nYou're ready to run the app:")
        print("  streamlit run app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the errors above before running the app.")
        print("If packages are missing, run:")
        print("  pip install -r requirements.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()
