from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import insert, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Union
from fast_api.operations.models import Wallet, Transaction
from fast_api.operations.schemas import WalletCreate


async def update_wallet_balance(
        session: AsyncSession,
        wallet_uuid: str,
        amount: Union[Decimal, float, int],
        operation_type: str
) -> Union[Decimal, float, int]:
    try:
        async with session.begin():
            query = await session.execute(select(Wallet).where(Wallet.id == wallet_uuid).with_for_update())
            wallet = query.scalar_one_or_none()
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet not found")
            current_balance = wallet.balance
            if operation_type == "deposit":
                new_balance = current_balance + amount
            elif operation_type == "withdraw":
                if current_balance < amount:
                    raise HTTPException(status_code=400, detail="Insufficient funds")
                new_balance = current_balance - amount
            record_trans = {
                'wallet_id': wallet_uuid,
                'transaction_type': operation_type,
                'amount': amount,
                'old_balance': current_balance,
                'new_balance': new_balance
            }
            await session.execute(insert(Transaction).values(record_trans))
            wallet.balance = new_balance
            await session.commit()
            return new_balance
    except Exception as e:
        await session.rollback()
        raise e


async def get_wallet_balance(session: AsyncSession, wallet_uuid: str) -> Union[Decimal, float, int]:
    query = await session.execute(select(Wallet).where(Wallet.id == wallet_uuid))
    wallet = query.scalar()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet.balance


async def get_activity_log(session: AsyncSession, wallet_uuid: str, limit: int = 30) -> Sequence[Transaction]:
    query = await session.execute(select(Transaction)
                                  .where(Transaction.wallet_id == wallet_uuid)
                                  .order_by(Transaction.timestamp.desc())
                                  .limit(limit))
    wallet_history = query.scalars().all()
    if not wallet_history:
        raise HTTPException(status_code=404, detail="Wallet history not found")
    return wallet_history


async def add_wallet(session: AsyncSession) -> WalletCreate:
    try:
        new_wallet = Wallet(balance=0)
        session.add(new_wallet)
        await session.commit()
        await session.refresh(new_wallet)
        return new_wallet.id
    except Exception as e:
        await session.rollback()
        raise e
