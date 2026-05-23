from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Transaction(BaseModel):
    referenceDate: datetime
    valeurDate: Optional[datetime] = None
    availDate: Optional[datetime] = None
    transactionCode: Optional[int] = None
    documentNr: Optional[str] = None
    notes: Optional[str] = None
    amountDebit: Optional[float] = None
    amountCredit: Optional[float] = None
    balance: Optional[float] = None
