import pandas as pd

# Load the raw dataset
df = pd.read_excel("../data/financial_expense_data.xlsx")

# Check basic information
print("Original rows:", len(df))
print("Missing values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Convert Date column to proper date format
df["Date"] = pd.to_datetime(df["Date"])

# Make sure Amount and Budget are numeric
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")

# Remove rows with missing important values
df = df.dropna(subset=[
    "Date",
    "Department",
    "Expense Category",
    "Amount",
    "Budget"
])

# Create Month column
df["Month"] = df["Date"].dt.strftime("%b")

# Create Budget Variance
df["Budget Variance"] = df["Budget"] - df["Amount"]

# Create Budget Utilization %
df["Budget Utilization %"] = (
    df["Amount"] / df["Budget"] * 100
).round(2)

# Save cleaned dataset
df.to_excel(
    "../data/financial_expense_data_cleaned.xlsx",
    index=False
)

print("\nData cleaning completed!")
print("Final rows:", len(df))
print("Cleaned file saved successfully.")