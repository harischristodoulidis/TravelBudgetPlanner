import openpyxl
from pathlib import Path
from .models import Transaction

EXCEL_PATH = Path(__file__).parent.parent.parent / "038325_1080103832500-0_ΤΑΜΙΕΥΤΗΡΙΟ.xlsx"


def load_transactions() -> list[Transaction]:
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = rows[0]
    transactions = []
    for row in rows[1:]:
        data = dict(zip(headers, row))
        if data.get("referenceDate") is None:
            continue
        transactions.append(Transaction(**data))
    return transactions
