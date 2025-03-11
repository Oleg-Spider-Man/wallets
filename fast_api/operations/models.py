from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, UUID, NUMERIC, ForeignKey, Enum, DateTime
from fast_api.database import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(UUID, primary_key=True, default=uuid4)
    balance = Column(NUMERIC(15, 2))


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID, primary_key=True, default=uuid4)
    wallet_id = Column(UUID, ForeignKey("wallets.id"))
    amount = Column(NUMERIC(15, 2))
    transaction_type = Column(Enum("deposit", "withdraw", name="transaction_types"))
    old_balance = Column(NUMERIC(15, 2))
    new_balance = Column(NUMERIC(15, 2))
    timestamp = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
