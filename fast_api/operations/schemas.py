from datetime import datetime, timezone
from decimal import Decimal
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class OperationRequest(BaseModel):
    operation_type: str
    amount: Union[Decimal, float, int]


class ActivityLog(BaseModel):
    id: UUID
    wallet_id: UUID
    amount: Union[Decimal, float, int]
    transaction_type: str
    old_balance: Union[Decimal, float, int]
    new_balance: Union[Decimal, float, int]
    timestamp: datetime = datetime.now(timezone.utc)
