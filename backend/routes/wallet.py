from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.services.wallet import get_wallet_balance, generate_wallet

router = APIRouter()


class WalletBalanceResponse(BaseModel):
    address: str
    balance: str
    currency: str


class GenerateWalletResponse(BaseModel):
    address: str
    private_key: str


@router.get('/{address}/balance', response_model=WalletBalanceResponse)
async def get_balance(address: str):
    try:
        balance = await get_wallet_balance(address)
        return WalletBalanceResponse(
            address=address,
            balance=balance,
            currency='MATIC'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to get balance: {str(e)}'
        )


@router.post('/generate', response_model=GenerateWalletResponse)
async def create_wallet():
    try:
        wallet = generate_wallet()
        return GenerateWalletResponse(
            address=wallet['address'],
            private_key=wallet['private_key']
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to generate wallet: {str(e)}'
        )