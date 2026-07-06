import pytest

from app import load_data


@pytest.fixture(scope="module")
def df():
    return load_data()


def test_load_data_shape(df):
    assert len(df) == 482


def test_load_data_parses_date(df):
    assert str(df["date"].dtype) == "datetime64[ns]"
