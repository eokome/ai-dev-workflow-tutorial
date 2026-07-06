import pytest

from app import load_data, compute_kpis, compute_monthly_trend, compute_category_breakdown, compute_region_breakdown


@pytest.fixture(scope="module")
def df():
    return load_data()


def test_load_data_shape(df):
    assert len(df) == 482


def test_load_data_parses_date(df):
    assert str(df["date"].dtype) == "datetime64[ns]"


def test_compute_kpis(df):
    total_sales, total_orders = compute_kpis(df)
    assert total_sales == pytest.approx(116500.21, abs=0.01)
    assert total_orders == 482


def test_compute_monthly_trend(df):
    monthly = compute_monthly_trend(df)
    assert len(monthly) == 12
    assert list(monthly.columns) == ["month", "total_amount"]
    assert monthly["total_amount"].sum() == pytest.approx(116500.21, abs=0.01)


def test_compute_category_breakdown(df):
    category_df = compute_category_breakdown(df)
    assert category_df.iloc[0]["category"] == "Electronics"
    assert category_df.iloc[0]["total_amount"] == pytest.approx(42683.67, abs=0.01)
    assert list(category_df["total_amount"]) == sorted(category_df["total_amount"], reverse=True)


def test_compute_region_breakdown(df):
    region_df = compute_region_breakdown(df)
    assert set(region_df["region"]) == {"North", "South", "East", "West"}
    assert list(region_df["total_amount"]) == sorted(region_df["total_amount"], reverse=True)
