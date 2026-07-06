import pandas as pd
import streamlit as st

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


def main():
    st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
    st.title("ShopSmart Sales Dashboard")

    df = load_data()

    total_sales, total_orders = compute_kpis(df)
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")


if __name__ == "__main__":
    main()
