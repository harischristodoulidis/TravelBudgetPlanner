from contextlib import asynccontextmanager
from fastapi import FastAPI
from .data import load_transactions
from .models import Transaction

transactions: list[Transaction] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global transactions
    transactions = load_transactions()
    yield


app = FastAPI(title="TravelBudgetPlanner", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "transactions_loaded": len(transactions)}


@app.get("/transactions", response_model=list[Transaction])
def get_transactions():
    return transactions


@app.get("/transactions/summary")
def get_summary():
    total_debit = sum(t.amountDebit or 0 for t in transactions)
    total_credit = sum(t.amountCredit or 0 for t in transactions)
    return {
        "count": len(transactions),
        "total_debit": round(total_debit, 2),
        "total_credit": round(total_credit, 2),
        "net": round(total_credit - total_debit, 2),
    }
