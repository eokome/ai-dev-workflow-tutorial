# Design: ShopSmart Sales Dashboard

**Date:** 2026-07-06
**Source requirements:** `prd/ecommerce-analytics.md`
**Tracking:** `TASKS.md` (TASK-1 through TASK-7)

## Summary

A single-page Streamlit dashboard that reads `data/sales-data.csv` and displays
Total Sales / Total Orders KPIs, a monthly sales trend line chart, and bar
charts of sales by category and by region. This covers Phase 1 of the PRD
only; Phase 2 items (auth, filtering, export, etc.) are explicitly out of
scope.

## Architecture

Matches the PRD's architecture diagram: no database or backend service. A
single Python script reads the CSV into Pandas on each run (cached across
reruns), computes aggregates in memory, and renders them with Plotly charts
inside Streamlit's layout.

```
User (browser)
      │
      ▼
Streamlit app (app.py)
  - KPI cards (Total Sales, Total Orders)
  - Line chart (monthly sales trend)
  - Bar charts (by category, by region)
      │
      ▼
Pandas aggregation (in-memory, computed in app.py)
      │
      ▼
data/sales-data.csv
```

## File Layout

```
app.py              # single file: data loading + UI
test_app.py         # pytest: verifies aggregation math against PRD's expected totals
requirements.txt    # streamlit, plotly, pandas — loose minimum versions
venv/               # virtual environment (gitignored)
data/sales-data.csv # already exists, no changes needed
```

A single `app.py` was chosen over splitting into modules, prioritizing
readability for a small, one-page dashboard over strict separation of
concerns (NFR-3's "modular structure" is satisfied at the function level
instead of the file level — see below).

## Components

**`load_data()`** — cached with `@st.cache_data` so the CSV is only read
once per session instead of on every Streamlit rerun. Parses the `date`
column as a real date type. Validates that the expected columns (`date`,
`order_id`, `product`, `category`, `region`, `quantity`, `unit_price`,
`total_amount`) are present; if not, calls `st.error()` with a clear message
and `st.stop()` rather than letting a raw KeyError/pandas traceback reach the
user. This is the lightweight version of the PRD's "validate CSV structure"
risk mitigation — column-presence checks, not a full schema-validation layer,
since the data source is a single known CSV rather than arbitrary user
uploads.

**`main()`** — computes aggregates directly with Pandas groupby/sum calls
and renders, top to bottom:
1. KPI cards (`st.metric`) for Total Sales (currency-formatted,
   `$X,XXX,XXX`) and Total Orders (row count).
2. A monthly sales trend line chart (Plotly Express `px.line`), grouping
   `total_amount` by month rather than by day — the PRD's own mockup shows
   monthly axis labels, and daily granularity across 482 rows / 12 months
   would be noisy.
3. Two bar charts side by side (`px.bar`): sales by category and sales by
   region, each sorted descending by value, each with hover tooltips showing
   exact values.

Both functions live in `app.py`. The UI code in `main()` is called only
under `if __name__ == "__main__": main()`. `streamlit run app.py` executes
the file as `__main__`, so this doesn't change runtime behavior — but it
means `test_app.py` can `import` `load_data()` without triggering Streamlit
UI calls that would error outside a live Streamlit session.

## Data Flow

CSV → `load_data()` (cached, column-validated) → aggregation via Pandas
groupby/sum in `main()` → Plotly Express builds each chart → Streamlit lays
out KPI cards, then the trend chart, then the two bar charts in columns,
matching the PRD's mockup layout.

## Error Handling

- Missing/malformed CSV columns: caught in `load_data()`, surfaced via
  `st.error()` + `st.stop()` with a human-readable message (satisfies
  NFR-2's "no training required" — a stakeholder seeing an error still gets
  a plain-English explanation, not a stack trace).
- No other error paths are anticipated: the CSV is a static, known-good file
  checked into the repo, not user-uploaded input, so extensive defensive
  validation is out of scope (per the "keep it simple" ground rule and
  YAGNI — there's no scenario in Phase 1 where the file changes shape at
  runtime).

## Testing

`test_app.py` (pytest) imports `load_data()` directly and asserts:
- Total sales sum matches the PRD's expected ~$116,500 (within a small
  tolerance).
- Total order count equals 482.
- Electronics is the top category by sales.

This is a fast regression check on the aggregation math, not a full test
suite — chart rendering and visual polish are still verified manually
against the PRD's acceptance-criteria checklist (TASK-6), since Plotly
output isn't practical to unit test.

## Milestone Mapping (TASKS.md)

| Task | Covered by |
|------|------------|
| TASK-1 | `venv/` setup, `requirements.txt`, project skeleton |
| TASK-2 | `load_data()` — CSV load, column validation, date parsing |
| TASK-3 | KPI cards in `main()` |
| TASK-4 | Monthly trend line chart in `main()` |
| TASK-5 | Category and region bar charts in `main()` |
| TASK-6 | `test_app.py` + manual acceptance-criteria pass |
| TASK-7 | Deployment — explicitly **out of scope for this plan**; the user deploys from `main` after merge |

## Ground Rules

- All work happens on the current `feature/sales-dashboard` branch — no git
  worktree.
- Dependencies are installed into a `venv/` virtual environment.
- Code favors simplicity and readability (single file, minimal abstraction,
  comments only where behavior is non-obvious, e.g. the `__name__` guard).
- Deployment (TASK-7) is the plan's final step, explicitly marked as the
  user's to execute — the plan stops before it.
