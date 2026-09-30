import pandas as pd
import random
from datetime import datetime, timedelta

# Number of records
num_records = 1000

departments = [
    "IT", "HR", "Finance", "Marketing",
    "Operations", "Sales", "Administration"
]

categories = [
    "Software", "Travel", "Office Supplies",
    "Advertising", "Training", "Utilities",
    "Equipment", "Professional Services"
]

vendors = [
    "Microsoft", "Amazon", "Google", "Dell",
    "Adobe", "TCS", "Infosys", "Local Vendor",
    "OfficeMart", "Tech Solutions"
]

payment_methods = [
    "Bank Transfer", "Credit Card", "Debit Card", "UPI"
]

descriptions = [
    "Software Subscription",
    "Business Travel",
    "Office Supplies Purchase",
    "Digital Advertising",
    "Employee Training",
    "Electricity Bill",
    "Computer Equipment",
    "Consulting Services"
]

start_date = datetime(2026, 1, 1)

data = []

for i in range(num_records):

    date = start_date + timedelta(days=random.randint(0, 364))

    department = random.choice(departments)
    category = random.choice(categories)
    vendor = random.choice(vendors)
    payment_method = random.choice(payment_methods)
    description = random.choice(descriptions)

    amount = random.randint(1000, 100000)

    budget = random.randint(
    int(amount * 0.6),
    int(amount * 1.1)
)

    data.append([
        date,
        department,
        category,
        vendor,
        description,
        amount,
        budget,
        payment_method
    ])

columns = [
    "Date",
    "Department",
    "Expense Category",
    "Vendor",
    "Description",
    "Amount",
    "Budget",
    "Payment Method"
]

df = pd.DataFrame(data, columns=columns)

# Sort by date
df = df.sort_values("Date")

# Save Excel file
df.to_excel(
    "../data/financial_expense_data.xlsx",
    index=False
)

print("Dataset created successfully!")
print(f"Total records: {len(df)}")
print("File saved as: data/financial_expense_data.xlsx")
