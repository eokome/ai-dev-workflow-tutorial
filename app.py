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
    trend_fig = px.line(monthly, x="month", y="total_amount", markers=True)
    trend_fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(trend_fig, use_container_width=True)


if __name__ == "__main__":
    main()
