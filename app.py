import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Financial Reporting & Expense Analysis",
    page_icon="💰",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_excel("data/financial_expense_data_cleaned.xlsx")

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("💰 Financial Reporting & Expense Analysis")

st.write(
    "An interactive dashboard for analyzing financial expenses, "
    "budget performance, departments, categories, and payment methods."
)


# ---------------------------------------------------------
# PROJECT PURPOSE
# ---------------------------------------------------------

st.subheader("🎯 Project Purpose")

st.write(
    "This project demonstrates how financial expense data can be "
    "prepared, analyzed, and presented through an interactive reporting "
    "dashboard. It helps users monitor spending, compare actual expenses "
    "with budgets, identify over-budget areas, and understand expense "
    "patterns across departments and categories."
)


# ---------------------------------------------------------
# DATASET OVERVIEW
# ---------------------------------------------------------

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Departments",
        df["Department"].nunique()
    )

with col3:
    st.metric(
        "Expense Categories",
        df["Expense Category"].nunique()
    )

with col4:
    st.metric(
        "Payment Methods",
        df["Payment Method"].nunique()
    )

st.info(
    "The dataset contains 1,000 synthetic financial expense transactions "
    "with information such as Date, Department, Expense Category, Vendor, "
    "Description, Amount, Budget, and Payment Method."
)


# ---------------------------------------------------------
# DATA PROCESSING & METHODOLOGY
# ---------------------------------------------------------

st.subheader("⚙️ Data Processing & Methodology")

with st.expander("View how the data was prepared"):

    st.markdown("""
    **1️⃣ Data Generation**

    Created a synthetic dataset containing **1,000 financial expense transactions**.

    Key fields included:

    - Date
    - Department
    - Expense Category
    - Vendor
    - Description
    - Amount
    - Budget
    - Payment Method


    **2️⃣ Data Cleaning**

    - Checked for missing values
    - Removed duplicate records
    - Converted date and numeric columns to appropriate data types
    - Removed records with missing key fields


    **3️⃣ Feature Engineering**

    - **Month** → Used for monthly expense trend analysis
    - **Budget Variance** → Budget − Actual Expense
    - **Budget Utilization %** → Actual Expense ÷ Budget × 100


    **4️⃣ Analysis & Visualization**

    - **Python & Pandas** → Data preparation and analysis
    - **Streamlit** → Interactive dashboard
    - **Plotly** → Interactive visualizations
    """)


# ---------------------------------------------------------
# DATA QUALITY CHECK
# ---------------------------------------------------------

st.subheader("✅ Data Quality Check")

missing_values = df.isnull().sum().sum()
duplicate_rows = df.duplicated().sum()
valid_records = len(df)

quality_col1, quality_col2, quality_col3 = st.columns(3)

with quality_col1:
    st.metric(
        "Missing Values",
        missing_values
    )

with quality_col2:
    st.metric(
        "Duplicate Rows",
        duplicate_rows
    )

with quality_col3:
    st.metric(
        "Valid Records",
        f"{valid_records:,}"
    )


# ---------------------------------------------------------
# KEY BUSINESS QUESTIONS
# ---------------------------------------------------------

st.subheader("💡 Key Business Questions")

st.markdown("""
This dashboard helps answer the following business questions:

- How much has the organization spent?
- How does actual spending compare with the allocated budget?
- Which departments have the highest expenses?
- Which expense categories contribute the most to total spending?
- Which departments or categories exceed their budgets?
- Which payment methods are used most frequently?
- How do expenses change over time?
- Where are the major spending and cost-control areas?
""")


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df[
    (df["Department"].isin(department_filter)) &
    (df["Expense Category"].isin(category_filter)) &
    (df["Payment Method"].isin(payment_filter))
].copy()


# ---------------------------------------------------------
# CHECK FILTERED DATA
# ---------------------------------------------------------

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change the filters."
    )

    st.stop()


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_expenses = filtered_df["Amount"].sum()

total_budget = filtered_df["Budget"].sum()

budget_utilization = (
    total_expenses / total_budget * 100
    if total_budget != 0
    else 0
)

budget_variance = total_budget - total_expenses


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("📌 Financial Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

with kpi2:
    st.metric(
        "Total Budget",
        f"₹{total_budget:,.0f}"
    )

with kpi3:
    st.metric(
        "Budget Utilization",
        f"{budget_utilization:.2f}%"
    )

with kpi4:
    st.metric(
        "Budget Variance",
        f"₹{budget_variance:,.0f}"
    )


# ---------------------------------------------------------
# MONTHLY EXPENSE TREND
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Monthly Expense Trend")

    monthly_expense = (
        filtered_df
        .groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    monthly_expense["Month"] = pd.Categorical(
        monthly_expense["Month"],
        categories=month_order,
        ordered=True
    )

    monthly_expense = monthly_expense.sort_values("Month")

    fig_month = px.line(
        monthly_expense,
        x="Month",
        y="Amount",
        markers=True,
        title="Monthly Expense Trend"
    )

    fig_month.update_layout(
        xaxis_title="Month",
        yaxis_title="Expense Amount (₹)"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )


# ---------------------------------------------------------
# EXPENSE DISTRIBUTION BY CATEGORY
# ---------------------------------------------------------

with col2:

    st.subheader("📊 Expense Distribution by Category")

    category_expense = (
        filtered_df
        .groupby("Expense Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    fig_category = px.bar(
        category_expense,
        x="Expense Category",
        y="Amount",
        title="Expense Distribution by Category"
    )

    fig_category.update_layout(
        xaxis_title="Expense Category",
        yaxis_title="Expense Amount (₹)",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ---------------------------------------------------------
# DEPARTMENT-WISE EXPENSES
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏢 Department-wise Expenses")

    department_expense = (
        filtered_df
        .groupby("Department")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    fig_department = px.bar(
        department_expense,
        x="Department",
        y="Amount",
        title="Department-wise Expense Analysis"
    )

    fig_department.update_layout(
        xaxis_title="Department",
        yaxis_title="Expense Amount (₹)"
    )

    st.plotly_chart(
        fig_department,
        use_container_width=True
    )


# ---------------------------------------------------------
# EXPENSE CATEGORY ANALYSIS
# ---------------------------------------------------------

with col2:

    st.subheader("📦 Expense Category Analysis")

    category_analysis = (
        filtered_df
        .groupby("Expense Category")
        .agg(
            Total_Spending=("Amount", "sum"),
            Transaction_Count=("Amount", "count"),
            Average_Transaction=("Amount", "mean")
        )
        .reset_index()
        .sort_values(
            "Total_Spending",
            ascending=False
        )
    )

    category_analysis["Average_Transaction"] = (
        category_analysis["Average_Transaction"]
        .round(2)
    )

    st.dataframe(
        category_analysis,
        use_container_width=True
    )


# ---------------------------------------------------------
# BUDGET VS ACTUAL
# ---------------------------------------------------------

st.subheader("🎯 Budget vs Actual Expenses")

budget_actual = (
    filtered_df
    .groupby("Department")[["Budget", "Amount"]]
    .sum()
    .reset_index()
)

budget_actual = budget_actual.rename(
    columns={
        "Amount": "Actual Expense"
    }
)

budget_actual_long = budget_actual.melt(
    id_vars="Department",
    value_vars=["Budget", "Actual Expense"],
    var_name="Type",
    value_name="Amount"
)

fig_budget = px.bar(
    budget_actual_long,
    x="Department",
    y="Amount",
    color="Type",
    barmode="group",
    title="Budget vs Actual Expenses by Department"
)

fig_budget.update_layout(
    xaxis_title="Department",
    yaxis_title="Amount (₹)",
    legend_title="Expense Type"
)

st.plotly_chart(
    fig_budget,
    use_container_width=True
)


# ---------------------------------------------------------
# DEPARTMENT VS EXPENSE CATEGORY HEATMAP
# ---------------------------------------------------------

st.subheader("🔥 Department vs Expense Category")

heatmap_data = (
    filtered_df
    .pivot_table(
        index="Department",
        columns="Expense Category",
        values="Amount",
        aggfunc="sum",
        fill_value=0
    )
)

fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=".0f",
    aspect="auto",
    title="Expense Distribution Across Departments and Categories"
)

fig_heatmap.update_layout(
    xaxis_title="Expense Category",
    yaxis_title="Department"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# ---------------------------------------------------------
# OVER-BUDGET DEPARTMENTS
# ---------------------------------------------------------

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
        ]
        .sort_values(
            "Overspending",
            ascending=False
        ),
        use_container_width=True
    )

else:

    st.success(
        "No departments are above their allocated budget."
    )


# ---------------------------------------------------------
# EXPENSE CATEGORY BUDGET ANALYSIS
# ---------------------------------------------------------

st.subheader("📊 Expense Category Budget Analysis")

category_budget = (
    filtered_df
    .groupby("Expense Category")[["Budget", "Amount"]]
    .sum()
    .reset_index()
)

category_budget["Variance"] = (
    category_budget["Budget"]
    - category_budget["Amount"]
)

category_budget["Status"] = category_budget["Variance"].apply(
    lambda x: "Over Budget" if x < 0 else "Within Budget"
)

st.dataframe(
    category_budget.sort_values(
        "Variance"
    ),
    use_container_width=True
)


# ---------------------------------------------------------
# PAYMENT METHOD ANALYSIS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("💳 Payment Method Analysis")

    payment_analysis = (
        filtered_df
        .groupby("Payment Method")
        .agg(
            Total_Spending=("Amount", "sum"),
            Transaction_Count=("Amount", "count"),
            Average_Transaction=("Amount", "mean")
        )
        .reset_index()
    )

    payment_analysis["Average_Transaction"] = (
        payment_analysis["Average_Transaction"]
        .round(2)
    )

    st.dataframe(
        payment_analysis,
        use_container_width=True
    )


# ---------------------------------------------------------
# PAYMENT METHOD CHART
# ---------------------------------------------------------

with col2:

    st.subheader("💰 Spending by Payment Method")

    payment_chart = (
        filtered_df
        .groupby("Payment Method")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Amount",
            ascending=False
        )
    )

    fig_payment = px.bar(
        payment_chart,
        x="Payment Method",
        y="Amount",
        title="Spending by Payment Method"
    )

    fig_payment.update_layout(
        xaxis_title="Payment Method",
        yaxis_title="Expense Amount (₹)"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


# ---------------------------------------------------------
# FINANCIAL SUMMARY
# ---------------------------------------------------------

st.subheader("📋 Financial Summary")

highest_category = (
    filtered_df
    .groupby("Expense Category")["Amount"]
    .sum()
    .idxmax()
)

highest_category_amount = (
    filtered_df
    .groupby("Expense Category")["Amount"]
    .sum()
    .max()
)

highest_department = (
    filtered_df
    .groupby("Department")["Amount"]
    .sum()
    .idxmax()
)

highest_department_amount = (
    filtered_df
    .groupby("Department")["Amount"]
    .sum()
    .max()
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.info(
        f"**Highest Expense Category:** "
        f"{highest_category} "
        f"(₹{highest_category_amount:,.0f})"
    )

with summary_col2:

    st.info(
        f"**Highest Spending Department:** "
        f"{highest_department} "
        f"(₹{highest_department_amount:,.0f})"
    )


# ---------------------------------------------------------
# KEY INSIGHTS
# ---------------------------------------------------------

st.subheader("💡 Key Insights")

highest_payment_method = (
    filtered_df
    .groupby("Payment Method")["Amount"]
    .sum()
    .idxmax()
)

highest_payment_amount = (
    filtered_df
    .groupby("Payment Method")["Amount"]
    .sum()
    .max()
)

st.markdown(
    f"""
    - 📌 **Highest Expense Category:** {highest_category} 
      with spending of **₹{highest_category_amount:,.0f}**.

    - 🏢 **Highest Spending Department:** {highest_department} 
      with spending of **₹{highest_department_amount:,.0f}**.

    - 💳 **Highest Spending Payment Method:** {highest_payment_method} 
      with spending of **₹{highest_payment_amount:,.0f}**.

    - ⚠️ **Over-Budget Departments:** 
      {len(over_budget)} department(s) are currently above their allocated budget.

    - 📊 The dashboard can be filtered by **Department, Expense Category, 
      and Payment Method** to perform more detailed analysis.
    """
)


# ---------------------------------------------------------
# DETAILED TRANSACTIONS
# ---------------------------------------------------------

with st.expander("📋 View Detailed Expense Transactions"):

    st.write(
        f"Showing **{len(filtered_df):,}** filtered records."
    )

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


# ---------------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------------

st.subheader("⬇️ Download Filtered Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="filtered_financial_expense_data.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Financial Reporting & Expense Analysis | "
    "Built with Python, Pandas, Streamlit and Plotly"
)
