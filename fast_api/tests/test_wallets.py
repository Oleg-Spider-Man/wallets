from unittest.mock import ANY
import pytest


@pytest.mark.asyncio
async def test_deposit_transaction(aclient):
    payload = {"operation_type": "deposit", "amount": 1000}
    response = await aclient.post("/money/api/v1/wallets/01234567-89ab-cdef-0123-456789abcdef/operation", json=payload)
    assert response.status_code == 200
    assert response.json() == ("транзакция выполнена успешно. "
                               "Баланс кошелька: 01234567-89ab-cdef-0123-456789abcdef, равен: 1000.00")


@pytest.mark.asyncio
async def test_withdraw_transaction(aclient):
    payload = {"operation_type": "withdraw", "amount": 500}
    response = await aclient.post("/money/api/v1/wallets/01234567-89ab-cdef-0123-456789abcdef/operation", json=payload)
    assert response.status_code == 200
    assert response.json() == ("транзакция выполнена успешно. "
                               "Баланс кошелька: 01234567-89ab-cdef-0123-456789abcdef, равен: 500.00")


@pytest.mark.asyncio
async def test_insufficient_funds(aclient):
    payload = {"operation_type": "withdraw", "amount": 500000}
    response = await aclient.post("/money/api/v1/wallets/01234567-89ab-cdef-0123-456789abcdef/operation", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "400: Insufficient funds"}


@pytest.mark.asyncio
async def test_wallet_not_found(aclient):
    payload = {"operation_type": "withdraw", "amount": 500000}
    response = await aclient.post("/money/api/v1/wallets/01234567-89ab-cdef-0124-456789abcdef/operation", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "404: Wallet not found"}


@pytest.mark.asyncio
async def test_get_wallet_balance(aclient):
    response = await aclient.get("/money/api/v1/wallets/01234567-89ab-cdef-0123-456789abcdef")
    assert response.status_code == 200
    assert response.json() == "Баланс кошелька: 01234567-89ab-cdef-0123-456789abcdef, равен: 500.00"


@pytest.mark.asyncio
async def test_activity_logs(aclient):
    response = await aclient.get("/money/api/v1/activity_log/01234567-89ab-cdef-0123-456789abcdef", params={"limit": 2})
    result = response.json()
    timestamps = [item["timestamp"] for item in result]
    assert timestamps == sorted(timestamps, reverse=True)
    assert response.status_code == 200
    assert result == [
        {
          "id": ANY,
          "wallet_id": "01234567-89ab-cdef-0123-456789abcdef",
          "amount": "1000.00",
          "transaction_type": "deposit",
          "old_balance": "0.00",
          "new_balance": "1000.00",
          "timestamp": ANY
         },
        {
           "id": ANY,
           "wallet_id": "01234567-89ab-cdef-0123-456789abcdef",
           "amount": "500.00",
           "transaction_type": "withdraw",
           "old_balance": "1000.00",
           "new_balance": "500.00",
           "timestamp": ANY
        },
    ]


@pytest.mark.asyncio
async def test_logs_not_fond(aclient):
    response = await aclient.get("/money/api/v1/activity_log/01238567-89ab-cdef-0123-456789abcdef", params={"limit": 2})
    assert response.status_code == 400
    assert response.json() == {"detail": "404: Wallet history not found"}


@pytest.mark.asyncio
async def test_create_wallet(aclient):
    response = await aclient.post("/money/api/v1/create_wallet/")
    assert response.status_code == 200
    assert len(response.json()) == 105
