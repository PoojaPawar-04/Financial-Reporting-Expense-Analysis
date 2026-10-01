import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Financial Reporting & Expense Analysis",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_excel("data/financial_expense_data_cleaned.xlsx")

# Make sure Date is datetime
df["Date"] = pd.to_datetime(df["Date"])

# =========================================================
# TITLE
# =========================================================

st.title("💰 Financial Reporting & Expense Analysis")

st.write(
    "Analyze business expenses, budgets, and financial performance "
    "through an interactive reporting dashboard."
)

# =========================================================
# PROJECT PURPOSE
# =========================================================

st.subheader("📌 Project Purpose")

st.info(
    "This project demonstrates how financial expense data can be "
    "prepared, analyzed, and presented through an interactive reporting "
    "dashboard. It helps users monitor spending, compare actual expenses "
    "with budgets, identify over-budget areas, and understand expense "
    "patterns across departments and categories."
)

# =========================================================
# DATASET OVERVIEW
# =========================================================

st.subheader("📊 Dataset Overview")

overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)

with overview_col1:
    st.metric("Total Records", f"{len(df):,}")

with overview_col2:
    st.metric("Departments", df["Department"].nunique())

with overview_col3:
    st.metric(
        "Expense Categories",
        df["Expense Category"].nunique()
    )

with overview_col4:
    st.metric(
        "Payment Methods",
        df["Payment Method"].nunique()
    )

st.info(
    "This dashboard analyzes a synthetic dataset of 1,000 financial "
    "expense transactions. The data contains transaction dates, "
    "departments, expense categories, vendors, amounts, budgets, "
    "and payment methods."
)

# =========================================================
# DATA PROCESSING & METHODOLOGY
# =========================================================

st.subheader("🔄 Data Processing & Methodology")

with st.expander("View how the data was prepared"):

    st.markdown("""
    **1. Data Generation**

    - Created a synthetic dataset containing 1,000 financial expense transactions.
    - Dataset includes Date, Department, Expense Category, Vendor,
      Description, Amount, Budget, and Payment Method.

    **2. Data Cleaning**

    - Checked for missing values.
    - Removed duplicate records.
    - Converted date and numeric columns to appropriate data types.
    - Removed records with missing key fields.

    **3. Feature Engineering**

    - **Month** → Used for monthly expense trend analysis.
    - **Budget Variance** → Budget − Actual Expense.
    - **Budget Utilization %** → Actual Expense ÷ Budget × 100.

    **4. Analysis & Visualization**

    - Used **Python and Pandas** for data preparation and analysis.
    - Used **Streamlit and Plotly** to build interactive financial
      reports and visualizations.
    """)

# =========================================================
# DATA QUALITY CHECK
# =========================================================

st.subheader("✅ Data Quality Check")

quality_col1, quality_col2, quality_col3 = st.columns(3)

with quality_col1:
    st.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

with quality_col2:
    st.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

with quality_col3:
    st.metric(
        "Valid Records",
        f"{len(df):,}"
    )

# =========================================================
# KEY BUSINESS QUESTIONS
# =========================================================

st.subheader("🎯 Key Business Questions")

st.markdown("""
This dashboard helps answer the following financial reporting questions:

- 💰 How much has the organization spent?
- 🎯 How does actual spending compare with the allocated budget?
- 🏢 Which departments have the highest expenses?
- 📂 Which expense categories contribute most to total spending?
- ⚠️ Which departments or categories are exceeding their budgets?
- 💳 Which payment methods are used most for business expenses?
- 📈 How do expenses change over time?
- 📊 Where are the major areas of spending and potential cost control?
""")

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")

department_filter = st.sidebar.multiselect(
    "Select Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

category_filter = st.sidebar.multiselect(
    "Select Expense Category",
    options=sorted(df["Expense Category"].unique()),
    default=sorted(df["Expense Category"].unique())
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=sorted(df["Payment Method"].unique()),
    default=sorted(df["Payment Method"].unique())
)

filtered_df = df[
    (df["Department"].isin(department_filter)) &
    (df["Expense Category"].isin(category_filter)) &
    (df["Payment Method"].isin(payment_filter))
]

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_expenses = filtered_df["Amount"].sum()

total_budget = filtered_df["Budget"].sum()

budget_variance = filtered_df["Budget Variance"].sum()

if total_budget > 0:
    budget_utilization = (
        total_expenses / total_budget
    ) * 100
else:
    budget_utilization = 0

# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

with col2:
    st.metric(
        "🎯 Total Budget",
        f"₹{total_budget:,.0f}"
    )

with col3:
    st.metric(
        "📊 Budget Utilization",
        f"{budget_utilization:.2f}%"
    )

with col4:
    st.metric(
        "📈 Budget Variance",
        f"₹{budget_variance:,.0f}"
    )

# =========================================================
# TREND & DISTRIBUTION
# =========================================================

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# Monthly Expense Trend
# ---------------------------------------------------------

with col1:

    st.subheader("📈 Monthly Expense Trend")

    monthly_expenses = (
        filtered_df
        .groupby("Month")["Amount"]
        .sum()
        .reindex([
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ])
        .dropna()
    )

    st.line_chart(monthly_expenses)

# ---------------------------------------------------------
# Expense Distribution
# ---------------------------------------------------------

with col2:

    st.subheader("🥧 Expense Distribution by Category")

    category_distribution = (
        filtered_df
        .groupby("Expense Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_distribution,
        names="Expense Category",
        values="Amount",
        title="Expense Distribution by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# DEPARTMENT & CATEGORY ANALYSIS
# =========================================================

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# Department-wise Expenses
# ---------------------------------------------------------

with col1:

    st.subheader("🏢 Department-wise Expenses")

    department_expenses = (
        filtered_df
        .groupby("Department")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(department_expenses)

# ---------------------------------------------------------
# Expense Category Analysis
# ---------------------------------------------------------

with col2:

    st.subheader("📂 Expense Category Analysis")

    category_expenses = (
        filtered_df
        .groupby("Expense Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_expenses)

# =========================================================
# BUDGET VS ACTUAL
# =========================================================

st.subheader("🎯 Budget vs Actual Expenses")

budget_actual = (
    filtered_df
    .groupby("Department")[["Budget", "Amount"]]
    .sum()
)

budget_actual = budget_actual.rename(
    columns={"Amount": "Actual Expense"}
)

st.bar_chart(budget_actual)

# =========================================================
# DEPARTMENT VS EXPENSE CATEGORY HEATMAP
# =========================================================

st.subheader("🔥 Department vs Expense Category")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Amount",
        index="Department",
        columns="Expense Category",
        aggfunc="sum",
        fill_value=0
    )
)

fig = px.imshow(
    heatmap_data,
    text_auto=".0f",
    aspect="auto",
    title="Department-wise Expense by Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# OVER-BUDGET DEPARTMENTS
# =========================================================

st.subheader("⚠️ Over-Budget Departments")

department_budget = (
    filtered_df
    .groupby("Department")[["Budget", "Amount"]]
    .sum()
)

department_budget["Variance"] = (
    department_budget["Budget"]
    - department_budget["Amount"]
)

over_budget = department_budget[
    department_budget["Variance"] < 0
].copy()

if len(over_budget) > 0:

    over_budget["Overspending"] = (
        over_budget["Variance"].abs()
    )

    st.warning(
        f"{len(over_budget)} department(s) are above "
        f"their allocated budget."
    )

    st.dataframe(
        over_budget[
            [
                "Budget",
                "Amount",
                "Variance",
                "Overspending"
            ]
        ].sort_values(
            "Overspending",
            ascending=False
        ),
        use_container_width=True
    )

else:

    st.success(
        "No departments are above their allocated budget."
    )

# =========================================================
# EXPENSE CATEGORY BUDGET ANALYSIS
# =========================================================

st.subheader("📂 Expense Category Budget Analysis")

category_budget = (
    filtered_df
    .groupby("Expense Category")[["Budget", "Amount"]]
    .sum()
)

category_budget["Variance"] = (
    category_budget["Budget"]
    - category_budget["Amount"]
)

category_budget["Status"] = category_budget["Variance"].apply(
    lambda x: "⚠️ Over Budget"
    if x < 0
    else "✅ Within Budget"
)

st.dataframe(
    category_budget.sort_values("Variance"),
    use_container_width=True
)

# =========================================================
# PAYMENT METHOD ANALYSIS
# =========================================================

st.subheader("💳 Payment Method Analysis")

payment_analysis = (
    filtered_df
    .groupby("Payment Method")
    .agg(
        Total_Spending=("Amount", "sum"),
        Transaction_Count=("Amount", "count"),
        Average_Transaction=("Amount", "mean")
    )
)

payment_analysis["Total_Spending"] = (
    payment_analysis["Total_Spending"].round(0)
)

payment_analysis["Average_Transaction"] = (
    payment_analysis["Average_Transaction"].round(0)
)

st.dataframe(
    payment_analysis,
    use_container_width=True
)

# =========================================================
# PAYMENT METHOD CHART
# =========================================================

st.subheader("💳 Spending by Payment Method")

payment_spending = (
    filtered_df
    .groupby("Payment Method")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(payment_spending)

# =========================================================
# FINANCIAL SUMMARY
# =========================================================

st.subheader("📊 Financial Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.write("**Highest Expense Category**")

    highest_category = (
        filtered_df
        .groupby("Expense Category")["Amount"]
        .sum()
        .idxmax()
    )

    st.info(highest_category)

with summary_col2:

    st.write("**Highest Spending Department**")

    highest_department = (
        filtered_df
        .groupby("Department")["Amount"]
        .sum()
        .idxmax()
    )

    st.info(highest_department)

# =========================================================
# KEY INSIGHTS
# =========================================================

st.subheader("📌 Key Insights")

highest_category_amount = (
    filtered_df
    .groupby("Expense Category")["Amount"]
    .sum()
    .max()
)

highest_department_amount = (
    filtered_df
    .groupby("Department")["Amount"]
    .sum()
    .max()
)

highest_payment = (
    filtered_df
    .groupby("Payment Method")["Amount"]
    .sum()
    .idxmax()
)

over_budget_count = len(
    filtered_df
    .groupby("Department")
    .filter(
        lambda x:
        x["Amount"].sum() > x["Budget"].sum()
    )["Department"]
    .unique()
)

st.markdown(
    f"""
    - 📂 **Highest Expense Category:** {highest_category}
      (₹{highest_category_amount:,.0f})

    - 🏢 **Highest Spending Department:** {highest_department}
      (₹{highest_department_amount:,.0f})

    - 💳 **Highest Spending Payment Method:** {highest_payment}

    - ⚠️ **Over-Budget Departments:** {over_budget_count}
    """
)

# =========================================================
# DETAILED TRANSACTIONS
# =========================================================

st.subheader("📋 Detailed Expense Transactions")

st.dataframe(
    filtered_df[
        [
            "Date",
            "Department",
            "Expense Category",
            "Vendor",
            "Description",
            "Amount",
            "Budget",
            "Budget Variance",
            "Budget Utilization %",
            "Payment Method"
        ]
    ],
    use_container_width=True
)

# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Financial Data",
    data=csv_data,
    file_name="filtered_financial_data.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Financial Reporting & Expense Analysis | "
    "Built with Python, Pandas, Streamlit and Plotly"
)
