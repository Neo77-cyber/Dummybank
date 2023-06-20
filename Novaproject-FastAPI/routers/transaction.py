from utils.token import get_user, authenticate_token
from fastapi import Depends, HTTPException, APIRouter
from typing import Dict
from database.models import User,Portfolio, Transaction
from database.hash import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from database.schemas import TransactionCreateRequest,TransactionResponse



router = APIRouter(prefix='/transaction',
                   tags=['transaction'])

@router.post("/create_transaction", response_model=TransactionResponse,
                                    description='Create a transaction with a valid pin')
async def create_transaction(new_transaction: TransactionCreateRequest, user: User = Depends(authenticate_token)):
    

        portfolio = await Portfolio.filter(user=user).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        if new_transaction.transfer_pin != portfolio.pin:
            raise HTTPException(status_code=400, detail="Invalid PIN.")

        if new_transaction.amount_to_transfer > portfolio.account_total:
            raise HTTPException(status_code=400, detail="Insufficient funds.")

        beneficiary_username = new_transaction.beneficiary_name
        beneficiary = await get_user(beneficiary_username)
        if not beneficiary:
            raise HTTPException(status_code=404, detail="Beneficiary not found.")

        transaction = await Transaction.create(user=user, beneficiary_name=beneficiary_username,
                                               amount_to_transfer=new_transaction.amount_to_transfer,
                                               transfer_pin=new_transaction.transfer_pin)

        portfolio.account_total -= new_transaction.amount_to_transfer
        await portfolio.save()

        beneficiary_portfolio = await Portfolio.filter(user=beneficiary).first()

        if not beneficiary_portfolio:
            raise HTTPException(status_code=404, detail="Beneficiary portfolio not found.")
        beneficiary_portfolio.account_total += new_transaction.amount_to_transfer
        await beneficiary_portfolio.save()

        response = TransactionResponse(user=user.username, beneficiary_name=beneficiary_username,
                                       amount_to_transfer=new_transaction.amount_to_transfer,
                                       transfer_pin=new_transaction.transfer_pin)
        
        return response

    


    
