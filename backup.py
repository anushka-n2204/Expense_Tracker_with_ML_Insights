"""
Backup utility for expense tracker
Creates backups of database and exports data
"""
import shutil
import os
from datetime import datetime
import pandas as pd
from database import Database


def backup_database(backup_dir="backups"):
    """Create a backup of the database"""
    os.makedirs(backup_dir, exist_ok=True)
    
    if not os.path.exists("data/expenses.db"):
        print("No database file found to backup")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/expenses_backup_{timestamp}.db"
    
    shutil.copy2("data/expenses.db", backup_file)
    print(f"✅ Database backed up to: {backup_file}")
    return backup_file


def backup_to_csv(backup_dir="backups"):
    """Export all expenses to CSV backup"""
    os.makedirs(backup_dir, exist_ok=True)
    
    db = Database()
    expenses = db.get_all_expenses()
    
    if expenses.empty:
        print("No expenses to backup")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/expenses_backup_{timestamp}.csv"
    
    expenses.to_csv(backup_file, index=False)
    print(f"✅ Expenses exported to: {backup_file}")
    print(f"   Total records: {len(expenses)}")
    return backup_file


def restore_from_csv(csv_file):
    """Restore expenses from CSV backup"""
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return False
    
    try:
        df = pd.read_csv(csv_file)
        db = Database()
        
        count = 0
        for _, row in df.iterrows():
            db.add_expense(
                date=row['date'],
                description=row['description'],
                category=row['category'],
                amount=row['amount'],
                is_anomaly=row.get('is_anomaly', 0)
            )
            count += 1
        
        print(f"✅ Restored {count} expenses from backup")
        return True
    except Exception as e:
        print(f"❌ Error restoring backup: {e}")
        return False


def list_backups(backup_dir="backups"):
    """List all available backups"""
    if not os.path.exists(backup_dir):
        print("No backups directory found")
        return []
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.endswith(('.db', '.csv')):
            filepath = os.path.join(backup_dir, file)
            size = os.path.getsize(filepath) / 1024  # KB
            modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'file': file,
                'path': filepath,
                'size_kb': f"{size:.2f}",
                'modified': modified.strftime("%Y-%m-%d %H:%M:%S")
            })
    
    return backups


if __name__ == "__main__":
    print("=== Expense Tracker Backup Utility ===\n")
    print("1. Backup database")
    print("2. Export to CSV")
    print("3. List backups")
    print("4. Restore from CSV")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == "1":
        backup_database()
    elif choice == "2":
        backup_to_csv()
    elif choice == "3":
        backups = list_backups()
        if backups:
            print("\nAvailable backups:")
            for backup in backups:
                print(f"  - {backup['file']}")
                print(f"    Size: {backup['size_kb']} KB")
                print(f"    Modified: {backup['modified']}\n")
        else:
            print("No backups found")
    elif choice == "4":
        csv_file = input("Enter CSV file path: ")
        restore_from_csv(csv_file)
    else:
        print("Invalid choice")
