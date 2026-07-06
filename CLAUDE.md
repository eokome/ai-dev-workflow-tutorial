# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repo is two things layered together:

1. **A tutorial** (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`) that teaches a PRD → TASKS.md → brainstorm → plan → build → deploy workflow using Claude Code's Superpowers skills.
2. **The project the tutorial has the student build**: a Streamlit sales dashboard for a fictional retailer, ShopSmart, specified in `prd/ecommerce-analytics.md` and tracked milestone-by-milestone in `TASKS.md`.

`v4/` is a stub pointing at the repo root — the tutorial used to live there; ignore it except to redirect.

## Commands

```bash
# One-time setup (venv/ is gitignored, not committed)
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# Run the dashboard
venv/bin/python -m streamlit run app.py
# or headless, for a scripted verification (no browser auto-open):
venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501

# Run all tests
venv/bin/python -m pytest test_app.py -v

# Run a single test
venv/bin/python -m pytest test_app.py::test_compute_kpis -v
```

There is no build/lint step — this is a single-script Streamlit app plus one test file.

## Architecture: `app.py`

`app.py` is deliberately one file, split into pure functions (data in, data out, no Streamlit calls) followed by a thin rendering layer:

- `load_data(path="data/sales-data.csv")` — cached with `@st.cache_data`, validates required columns against `REQUIRED_COLUMNS`, parses `date`. Missing columns surface via `st.error()` + `st.stop()` rather than a raw traceback.
- `compute_kpis(df)`, `compute_monthly_trend(df)`, `compute_category_breakdown(df)`, `compute_region_breakdown(df)` — pure functions, each independently unit-testable.
- `main()` — the only function that calls Streamlit UI (`st.metric`, `px.line`, `px.bar`, `st.columns`). It only runs under `if __name__ == "__main__":`.

That guard is why `test_app.py` can `import` the compute functions from `app.py` and test them directly, without a live Streamlit session, without mocks, and without a raw ImportError from Streamlit's session-state machinery. Keep new logic in pure, importable functions above `main()`, and keep `main()` itself thin (call a function, render its result) rather than inlining computation into the rendering code.

**Known environment gotcha:** `pd.to_datetime()` changed its default resolution in pandas 3.x, so `load_data()` explicitly casts to `.astype('datetime64[ns]')` — don't remove this cast, it's not redundant even though it looks like it.

## The TASKS.md workflow

`TASKS.md` is the durable, git-versioned task board — not the same thing as Claude Code's in-session todo list, which disappears at session end. It has three sections (To Do / In Progress / Done) and a shared **Definition of Done** template. When a milestone is completed, its entry in the Done section is expected to carry its own copy of the Definition-of-Done checklist (checked) plus the commit hash(es) that fulfilled it — see the TASK-1/TASK-2 entries for the expected format.

Every commit that implements part of a milestone includes that milestone's ID in the commit message (e.g. `TASK-3: add Total Sales and Total Orders KPI cards`). This is what makes `git log --grep="TASK-3"` a complete audit trail from requirement to code.

**Deployment (TASK-7) is a standing exception**: it's tracked on the board like any other milestone, but implementation plans in this repo mark it as user-executed, not something Claude runs. The user deploys manually to Streamlit Community Cloud from `main`, after merge — don't attempt to run or automate that step.

## Ground rules this repo's plans are built under

These come from the tutorial's prompting pattern (`workshop-build-deploy.md` §2.2) and apply to any implementation plan written for this project, not just the current one:

- Work happens directly on the feature branch — **no git worktree**.
- Dependencies live in `venv/` (gitignored).
- Deployment is planned but always marked as the user's step to execute, never Claude's.
