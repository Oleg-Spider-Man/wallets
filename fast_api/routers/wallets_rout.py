from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fast_api.dependencies import get_async_session
from fast_api.operations import schemas
from fast_api.operations.func_wallet import update_wallet_balance, get_wallet_balance, get_activity_log
from fast_api.operations.schemas import ActivityLog

router = APIRouter(
    prefix="/money",
    tags=["big_money"],
)


@router.post("/api/v1/wallets/{wallet_uuid}/operation",  response_model=str)
async def transaction(
        wallet_uuid: str,
        operation_request: schemas.OperationRequest,
        db: AsyncSession = Depends(get_async_session)
        ):
    amount = operation_request.amount
    operation_type = operation_request.operation_type
    try:
        result = await update_wallet_balance(db, wallet_uuid, amount, operation_type)
        return f"транзакция выполнена успешно. Баланс кошелька: {wallet_uuid}, равен: {result}"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/wallets/{wallet_uuid}",  response_model=str)
async def get_balance(wallet_uuid: str, db: AsyncSession = Depends(get_async_session)):
    try:
        cur_balance = await get_wallet_balance(db, wallet_uuid)
        return f"Баланс кошелька: {wallet_uuid}, равен: {cur_balance}"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/activity_log/{wallet_uuid}",  response_model=list[ActivityLog])
async def get_log(wallet_uuid: str, limit: int = Query(10, ge=0), db: AsyncSession = Depends(get_async_session)):
    try:
        result = await get_activity_log(db, wallet_uuid, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
