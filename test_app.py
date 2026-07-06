import pytest

from app import load_data, compute_kpis, compute_monthly_trend


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
