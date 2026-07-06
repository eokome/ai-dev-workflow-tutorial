import pandas as pd
import streamlit as st
import plotly.express as px

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


@st.cache_data
def load_data(path="data/sales-data.csv"):
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"sales-data.csv is missing required columns: {', '.join(missing)}")
        st.stop()
    # pandas 3.x changed pd.to_datetime's default resolution; pin to ns so the dtype is stable
    df["date"] = pd.to_datetime(df["date"]).astype('datetime64[ns]')
    return df


def compute_kpis(df):
    total_sales = df["total_amount"].sum()
    total_orders = len(df)
    return total_sales, total_orders


def compute_monthly_trend(df):
    monthly = df.groupby(pd.Grouper(key="date", freq="MS"))["total_amount"].sum().reset_index()
    monthly.columns = ["month", "total_amount"]
    return monthly


def compute_category_breakdown(df):
    return (
        df.groupby("category")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def compute_region_breakdown(df):
    return (
        df.groupby("region")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def main():
    st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
    st.title("ShopSmart Sales Dashboard")

    df = load_data()

    total_sales, total_orders = compute_kpis(df)
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")

    st.subheader("Sales Trend Over Time")
    monthly = compute_monthly_trend(df)
    trend_fig = px.line(
        monthly, x="month", y="total_amount", markers=True,
        labels={"month": "Month", "total_amount": "Sales ($)"},
    )
    trend_fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(trend_fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Sales by Category")
        category_df = compute_category_breakdown(df)
        category_fig = px.bar(
            category_df, x="category", y="total_amount",
            labels={"category": "Category", "total_amount": "Sales ($)"},
        )
        category_fig.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
        st.plotly_chart(category_fig, use_container_width=True)
    with col4:
        st.subheader("Sales by Region")
        region_df = compute_region_breakdown(df)
        region_fig = px.bar(
            region_df, x="region", y="total_amount",
            labels={"region": "Region", "total_amount": "Sales ($)"},
        )
        region_fig.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
        st.plotly_chart(region_fig, use_container_width=True)


if __name__ == "__main__":
    main()
