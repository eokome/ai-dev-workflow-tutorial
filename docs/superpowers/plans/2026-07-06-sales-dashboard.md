# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page Streamlit dashboard (`app.py`) that reads `data/sales-data.csv` and displays Total Sales / Total Orders KPIs, a monthly sales trend line chart, and category/region bar charts — matching `prd/ecommerce-analytics.md` and the design in `docs/superpowers/specs/2026-07-06-sales-dashboard-design.md`.

**Architecture:** A single `app.py` file with small, independently-testable pure functions (`load_data`, `compute_kpis`, `compute_monthly_trend`, `compute_category_breakdown`, `compute_region_breakdown`) that a `main()` function calls to render the UI. `main()` only runs under `if __name__ == "__main__"`, so `test_app.py` can import and test the pure functions without triggering Streamlit UI calls.

**Tech Stack:** Python 3.11+, Streamlit, Plotly Express, Pandas, pytest.

## Global Constraints

- All work happens on the current branch, `feature/sales-dashboard` — do not create a git worktree.
- Dependencies install into a `venv/` virtual environment in the project root.
- `requirements.txt` uses loose minimum versions (`>=`), not exact pins.
- Code stays in a single `app.py` file — no additional modules — favoring readability over strict separation of concerns.
- Every task's commit message includes its milestone ID (e.g. `TASK-1`), per `TASKS.md`'s Definition of Done.
- Every task must end with the app running locally via `streamlit run app.py` with no errors, per `TASKS.md`'s Definition of Done.
- After each task's commit, update `TASKS.md`: check that task's acceptance-criteria boxes and move its entry from "To Do" to "Done".
- Deployment (TASK-7) is explicitly **out of scope for this plan** — it is the last section below, marked for the user to execute manually. Stop before it.

---

### Task 1: Environment Setup & Project Skeleton (TASK-1)

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `app.py`

**Interfaces:**
- Produces: a runnable `app.py` with `main()` that renders a page title only. Later tasks add functions to this same file.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`
Expected: a `venv/` directory appears in the project root.

- [ ] **Step 2: Write requirements.txt**

```
streamlit>=1.38
plotly>=5.24
pandas>=2.2
pytest>=8.0
```

- [ ] **Step 3: Install dependencies**

Run: `venv/bin/pip install -r requirements.txt`
Expected: install completes with no errors.

- [ ] **Step 4: Write .gitignore**

```
venv/
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 5: Write the app.py skeleton**

```python
import streamlit as st


def main():
    st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
    st.title("ShopSmart Sales Dashboard")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Verify the app runs**

```bash
venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 &
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "App responded OK" || echo "App failed to respond"
kill %1
```
Expected: `App responded OK`.

- [ ] **Step 7: Update TASKS.md and commit**

In `TASKS.md`, check TASK-1's boxes and move its entry to the Done section.

```bash
git add requirements.txt .gitignore app.py TASKS.md
git commit -m "TASK-1: project skeleton and environment setup"
```

---

### Task 2: Data Loading and Validation (TASK-2)

**Files:**
- Modify: `app.py` (add `REQUIRED_COLUMNS` and `load_data()` above `main()`; call it from `main()`)
- Create: `test_app.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `load_data(path="data/sales-data.csv") -> pd.DataFrame` with a parsed `date` column (dtype `datetime64[ns]`). Later tasks' compute functions take this DataFrame as their only argument.

- [ ] **Step 1: Write the failing test**

```python
# test_app.py
import pytest

from app import load_data


@pytest.fixture(scope="module")
def df():
    return load_data()


def test_load_data_shape(df):
    assert len(df) == 482


def test_load_data_parses_date(df):
    assert str(df["date"].dtype) == "datetime64[ns]"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: FAIL with `ImportError: cannot import name 'load_data' from 'app'`.

- [ ] **Step 3: Implement load_data() in app.py**

```python
# app.py — add above main(), keep the existing import and main() below
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
    df["date"] = pd.to_datetime(df["date"])
    return df


def main():
    st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
    st.title("ShopSmart Sales Dashboard")

    df = load_data()
    st.write(f"Loaded {len(df)} rows.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: 2 passed. Streamlit may print a `missing ScriptRunContext` warning to stderr since `load_data()`'s `@st.cache_data` decorator is running outside a live Streamlit session — this is harmless and expected under pytest, not a failure.

- [ ] **Step 5: Verify the app runs**

```bash
venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 &
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "App responded OK" || echo "App failed to respond"
kill %1
```
Expected: `App responded OK`.

- [ ] **Step 6: Update TASKS.md and commit**

In `TASKS.md`, check TASK-2's boxes and move its entry to the Done section.

```bash
git add app.py test_app.py TASKS.md
git commit -m "TASK-2: load and validate sales-data.csv"
```

---

### Task 3: KPI Cards (TASK-3)

**Files:**
- Modify: `app.py` (add `compute_kpis()`; replace the `st.write` placeholder in `main()` with KPI cards)
- Modify: `test_app.py` (add `test_compute_kpis`)

**Interfaces:**
- Consumes: `load_data()` from Task 2 — a DataFrame with a `total_amount` column.
- Produces: `compute_kpis(df) -> tuple[float, int]` returning `(total_sales, total_orders)`.

- [ ] **Step 1: Write the failing test**

```python
# test_app.py — add below the existing tests
from app import compute_kpis


def test_compute_kpis(df):
    total_sales, total_orders = compute_kpis(df)
    assert total_sales == pytest.approx(116500.21, abs=0.01)
    assert total_orders == 482
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: FAIL with `ImportError: cannot import name 'compute_kpis' from 'app'`.

- [ ] **Step 3: Implement compute_kpis() and wire it into main()**

```python
# app.py — add below load_data()
def compute_kpis(df):
    total_sales = df["total_amount"].sum()
    total_orders = len(df)
    return total_sales, total_orders
```

```python
# app.py — replace the body of main() from Task 2
def main():
    st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
    st.title("ShopSmart Sales Dashboard")

    df = load_data()

    total_sales, total_orders = compute_kpis(df)
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: 3 passed.

- [ ] **Step 5: Verify the app runs**

```bash
venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 &
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "App responded OK" || echo "App failed to respond"
kill %1
```
Expected: `App responded OK`. Manually confirm in a browser that Total Sales reads ~$116,500 and Total Orders reads 482.

- [ ] **Step 6: Update TASKS.md and commit**

In `TASKS.md`, check TASK-3's boxes and move its entry to the Done section.

```bash
git add app.py test_app.py TASKS.md
git commit -m "TASK-3: add Total Sales and Total Orders KPI cards"
```

---

### Task 4: Sales Trend Chart (TASK-4)

**Files:**
- Modify: `app.py` (add `import plotly.express as px`, add `compute_monthly_trend()`, add the trend chart to `main()`)
- Modify: `test_app.py` (add `test_compute_monthly_trend`)

**Interfaces:**
- Consumes: `load_data()` from Task 2 — a DataFrame with `date` (datetime64) and `total_amount` columns.
- Produces: `compute_monthly_trend(df) -> pd.DataFrame` with columns `["month", "total_amount"]`, one row per calendar month, sorted chronologically.

- [ ] **Step 1: Write the failing test**

```python
# test_app.py — add below the existing tests
from app import compute_monthly_trend


def test_compute_monthly_trend(df):
    monthly = compute_monthly_trend(df)
    assert len(monthly) == 12
    assert list(monthly.columns) == ["month", "total_amount"]
    assert monthly["total_amount"].sum() == pytest.approx(116500.21, abs=0.01)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: FAIL with `ImportError: cannot import name 'compute_monthly_trend' from 'app'`.

- [ ] **Step 3: Implement compute_monthly_trend() and wire it into main()**

```python
# app.py — add near the top with the other imports
import plotly.express as px
```

```python
# app.py — add below compute_kpis()
def compute_monthly_trend(df):
    monthly = df.groupby(pd.Grouper(key="date", freq="MS"))["total_amount"].sum().reset_index()
    monthly.columns = ["month", "total_amount"]
    return monthly
```

```python
# app.py — add at the end of main(), after the KPI cards
    st.subheader("Sales Trend Over Time")
    monthly = compute_monthly_trend(df)
    trend_fig = px.line(monthly, x="month", y="total_amount", markers=True)
    trend_fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(trend_fig, use_container_width=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: 4 passed.

- [ ] **Step 5: Verify the app runs**

```bash
venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 &
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "App responded OK" || echo "App failed to respond"
kill %1
```
Expected: `App responded OK`. Manually confirm in a browser that the line chart shows 12 months with hover tooltips.

- [ ] **Step 6: Update TASKS.md and commit**

In `TASKS.md`, check TASK-4's boxes and move its entry to the Done section.

```bash
git add app.py test_app.py TASKS.md
git commit -m "TASK-4: add monthly sales trend line chart"
```

---

### Task 5: Category and Region Breakdown Charts (TASK-5)

**Files:**
- Modify: `app.py` (add `compute_category_breakdown()` and `compute_region_breakdown()`, add two side-by-side bar charts to `main()`)
- Modify: `test_app.py` (add `test_compute_category_breakdown` and `test_compute_region_breakdown`)

**Interfaces:**
- Consumes: `load_data()` from Task 2 — a DataFrame with `category`, `region`, and `total_amount` columns.
- Produces: `compute_category_breakdown(df) -> pd.DataFrame` with columns `["category", "total_amount"]`, sorted descending by `total_amount`. `compute_region_breakdown(df) -> pd.DataFrame` with columns `["region", "total_amount"]`, sorted descending by `total_amount`.

- [ ] **Step 1: Write the failing tests**

```python
# test_app.py — add below the existing tests
from app import compute_category_breakdown, compute_region_breakdown


def test_compute_category_breakdown(df):
    category_df = compute_category_breakdown(df)
    assert category_df.iloc[0]["category"] == "Electronics"
    assert category_df.iloc[0]["total_amount"] == pytest.approx(42683.67, abs=0.01)
    assert list(category_df["total_amount"]) == sorted(category_df["total_amount"], reverse=True)


def test_compute_region_breakdown(df):
    region_df = compute_region_breakdown(df)
    assert set(region_df["region"]) == {"North", "South", "East", "West"}
    assert list(region_df["total_amount"]) == sorted(region_df["total_amount"], reverse=True)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: FAIL with `ImportError: cannot import name 'compute_category_breakdown' from 'app'`.

- [ ] **Step 3: Implement both compute functions and wire them into main()**

```python
# app.py — add below compute_monthly_trend()
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
```

```python
# app.py — add at the end of main(), after the trend chart
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Sales by Category")
        category_df = compute_category_breakdown(df)
        category_fig = px.bar(category_df, x="category", y="total_amount")
        category_fig.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
        st.plotly_chart(category_fig, use_container_width=True)
    with col4:
        st.subheader("Sales by Region")
        region_df = compute_region_breakdown(df)
        region_fig = px.bar(region_df, x="region", y="total_amount")
        region_fig.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
        st.plotly_chart(region_fig, use_container_width=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: 6 passed.

- [ ] **Step 5: Verify the app runs**

```bash
venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 &
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "App responded OK" || echo "App failed to respond"
kill %1
```
Expected: `App responded OK`. Manually confirm both bar charts render side by side, each sorted highest to lowest, with hover tooltips.

- [ ] **Step 6: Update TASKS.md and commit**

In `TASKS.md`, check TASK-5's boxes and move its entry to the Done section.

```bash
git add app.py test_app.py TASKS.md
git commit -m "TASK-5: add category and region breakdown bar charts"
```

---

### Task 6: Testing and Refinement (TASK-6)

**Files:**
- Modify: `TASKS.md` (final acceptance-criteria pass)

**Interfaces:**
- Consumes: the complete `app.py` and `test_app.py` from Tasks 1–5.
- Produces: nothing new — this task verifies and polishes what already exists.

- [ ] **Step 1: Run the full test suite**

Run: `venv/bin/python -m pytest test_app.py -v`
Expected: 6 passed, 0 failed.

- [ ] **Step 2: Time the app's load**

```bash
time (venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 &
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "App responded OK"
kill %1)
```
Expected: `App responded OK`, with the total wall time well under the PRD's NFR-1 target of 5 seconds to load.

- [ ] **Step 3: Walk through the PRD's acceptance criteria manually**

Open the app in a browser (`venv/bin/python -m streamlit run app.py`) and confirm each item from `prd/ecommerce-analytics.md`'s Acceptance Criteria section:
- KPIs visible: Total Sales and Total Orders displayed prominently
- Trend chart works: line chart shows sales over time with correct data
- Category chart works: bar chart shows sales by category, sorted by value
- Region chart works: bar chart shows sales by region, sorted by value
- Data loads correctly: values match expected calculations from the CSV (~$116,500 total sales, 482 orders, Electronics as top category)
- No errors: dashboard runs without errors or warnings in the browser console or terminal
- Professional appearance: layout, labels, and spacing are suitable for an executive presentation

- [ ] **Step 4: Update TASKS.md and commit**

In `TASKS.md`, check TASK-6's boxes and move its entry to the Done section.

```bash
git add TASKS.md
git commit -m "TASK-6: verify acceptance criteria and performance targets"
```

---

## Handoff: Deployment (TASK-7) — Not part of this plan

Per the ground rules, deployment is **out of scope for this plan** and is yours to execute. When you're ready:

1. Merge `feature/sales-dashboard` into `main` (e.g. open a PR and merge, or merge locally).
2. From `main`, deploy to Streamlit Community Cloud following `NFR-5` in the PRD, pointing at `app.py`.
3. Confirm the public URL loads correctly, then check TASK-7's boxes and move it to Done in `TASKS.md`.

This plan's execution stops at the end of Task 6.
