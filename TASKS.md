# Tasks

This file tracks all work for the ShopSmart sales dashboard, from initial setup through deployment. See `prd/ecommerce-analytics.md` for full requirements.

## Definition of Done

Every milestone must meet all of the following before moving to Done:

- [ ] Acceptance criteria for the milestone are met
- [ ] App runs locally with `streamlit run app.py`
- [ ] Changes are committed with the milestone ID (e.g. `TASK-1`) in the commit message

---

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard to Streamlit Community Cloud with a public URL.
- [ ] App is deployed and reachable via a shareable public URL
- [ ] Deployed app matches local behavior (no missing data or broken charts)

---

## In Progress

_(none yet)_

---

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure and install required dependencies (Streamlit, Plotly, Pandas).
- [x] Project folder structure created (e.g. `app.py`, `data/`)
- [x] Dependencies installed and importable (streamlit, plotly, pandas)
- [x] `streamlit run app.py` launches a blank/placeholder app without errors

Definition of Done:
- [x] Acceptance criteria for the milestone are met
- [x] App runs locally with `streamlit run app.py`
- [x] Changes are committed with the milestone ID in the commit message

Commits: `0ae1d87`, `53ca4a6`

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` into a Pandas DataFrame and validate its structure.
- [x] CSV loads without errors and columns match the spec (date, order_id, product, category, region, quantity, unit_price, total_amount)
- [x] Date column is parsed as a proper date type
- [x] Row count matches expected 482 records

Definition of Done:
- [x] Acceptance criteria for the milestone are met
- [x] App runs locally with `streamlit run app.py`
- [x] Changes are committed with the milestone ID in the commit message

Commits: `b6d9e1a`

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as prominent KPI cards.
- [x] Total Sales displayed as formatted currency (~$116,500)
- [x] Total Orders displayed as a formatted count (482)
- [x] KPIs are visually prominent at the top of the dashboard

### TASK-4: Sales trend chart
Build an interactive line chart showing sales over time.
- [x] Line chart renders with time on the X-axis and sales amount on the Y-axis
- [x] Tooltips show exact values on hover
- [x] Chart data matches expected totals from the CSV

### TASK-5: Category and region breakdowns
Build bar charts showing sales by product category and by region.
- [x] Category bar chart shows all 5 categories, sorted highest to lowest, with tooltips
- [x] Region bar chart shows all 4 regions, sorted highest to lowest, with tooltips
- [x] Electronics appears as the top category, matching PRD expectations

### TASK-6: Testing and refinement
Verify the dashboard against the PRD's acceptance criteria and polish for presentation.
- [x] Dashboard loads within 5 seconds and charts render within 2 seconds
- [x] No errors or warnings appear when running the app
- [x] Layout and labels are professional and suitable for an executive presentation
