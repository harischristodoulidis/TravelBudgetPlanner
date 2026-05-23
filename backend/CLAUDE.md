# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

Hackathon project. **Keep code as simple as possible** — no over-engineering, no abstractions that aren't immediately needed. Flat structure, minimal dependencies.

This is a FastAPI backend for **TravelBudgetPlanner**, which reads and analyzes bank transaction data from a Greek savings account Excel file (`038325_1080103832500-0_ΤΑΜΙΕΥΤΗΡΙΟ.xlsx`, located at the repo root).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server (from backend/)
uvicorn main:app --reload

# Run a single test
pytest tests/test_name.py::test_function -v
```

## Data Source

The Excel file (`Φύλλο1` sheet) has ~1994 rows covering 2022, but only 417 rows have actual transaction data — the rest are `None`. Always filter out null rows before processing.

| Column | Type | Notes |
|---|---|---|
| `referenceDate` | datetime / None | |
| `valeurDate` | datetime / None | |
| `availDate` | datetime / None | |
| `transactionCode` | int / None | 15 unique codes (e.g. 69=card, 1=transfer) |
| `documentNr` | str / None | format: `NNN-NNNNNNNNNNNNNN` |
| `notes` | str / None | merchant name or description |
| `amountDebit` | float / None | expense |
| `amountCredit` | float / None | income |
| `balance` | float / None | running balance |

## Architecture

The app is structured to stay flat and simple:

- `main.py` — FastAPI app instantiation and all route definitions
- `data.py` — Excel loading and parsing logic (reads the `.xlsx` at startup)
- `models.py` — Pydantic models for request/response schemas
- `requirements.txt` — dependencies (`fastapi`, `uvicorn`, `openpyxl`, `pandas`)

Data is loaded once at startup into memory (no database). Routes query the in-memory dataset directly.
