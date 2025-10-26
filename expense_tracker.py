from datetime import datetime
from collections import defaultdict
import csv

# ===== Item Class =====
class Item:
    def __init__(self, name, price, quantity, category="General", date=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.date = date or datetime.now()

    def get_total_price(self):
        return self.price * self.quantity


# ===== ExpenseTracker Class =====
class ExpenseTracker:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity, category="General"):
        item = Item(name, price, quantity, category)
        self.items.append(item)
        print(f"\n✅ Added: {name}, {quantity} x {price} in category '{category}'.")
        self.save_to_csv()  # 💾 Auto-save after adding

    def show_items(self):
        if not self.items:
            print("\n⚠️ No expenses yet.")
            return

        print("\n📋 Items in your Expense List:")
        print("{:<15} {:<10} {:<10} {:<10} {:<15} {:<20}".format(
            "Name", "Price", "Quantity", "Total", "Category", "Date"
        ))
        for item in self.items:
            print("{:<15} {:<10} {:<10} {:<10} {:<15} {:<20}".format(
                item.name,
                item.price,
                item.quantity,
                item.get_total_price(),
                item.category,
                item.date.strftime("%Y-%m-%d %H:%M")
            ))

    def calculate_total(self):
        total = sum(item.get_total_price() for item in self.items)
        print(f"\n💰 Total Expense: {total}")

    def category_summary(self):
        if not self.items:
            print("\n⚠️ No expenses yet.")
            return

        summary = defaultdict(int)
        for item in self.items:
            summary[item.category] += item.get_total_price()

        print("\n📊 Category-wise Summary:")
        for category, amount in summary.items():
            print(f"{category}: {amount}")

    def save_to_csv(self, filename="expenses.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Price", "Quantity", "Category", "Date"])
            for item in self.items:
                writer.writerow([
                    item.name,
                    item.price,
                    item.quantity,
                    item.category,
                    item.date.strftime("%Y-%m-%d %H:%M")
                ])
        print(f"\n💾 Expenses saved to {filename}")

    def load_from_csv(self, filename="expenses.csv"):
        try:
            with open(filename, "r") as f:
                 reader = csv.DictReader(f)
                 for row in reader:
                     item = Item(
                        name=row["Name"],
                        price=float(row["Price"]),
                        quantity=int(row["Quantity"]),
                        category=row["Category"],
                        date=datetime.strptime(row["Date"], "%Y-%m-%d %H:%M")
                     )

                     self.items.append(item)
            print(f"📂 Loaded {len(self.items)} expenses from {filename}")

        except FileNotFoundError:
            print("⚠️ No saved data found — starting fresh.")

# ===== CLI Interaction =====
def main():
    tracker = ExpenseTracker()
    tracker.load_from_csv()  # 🧠 Auto-load at startup
    
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. ➕ Add Expense")
        print("2. 📋 Show Expenses")
        print("3. 💰 Total Expense")
        print("4. 📊 Category Summary")
        print("5. 💾 Save to CSV")
        print("6. ❌ Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Item name: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            category = input("Category (default 'General'): ") or "General"
            tracker.add_item(name, price, quantity, category)

        elif choice == "2":
            tracker.show_items()

        elif choice == "3":
            tracker.calculate_total()

        elif choice == "4":
            tracker.category_summary()

        elif choice == "5":
            tracker.save_to_csv()

        elif choice == "6":
            tracker.save_to_csv()
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
