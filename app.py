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


def main():
    st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
    st.title("ShopSmart Sales Dashboard")

    df = load_data()
    st.write(f"Loaded {len(df)} rows.")


if __name__ == "__main__":
    main()
