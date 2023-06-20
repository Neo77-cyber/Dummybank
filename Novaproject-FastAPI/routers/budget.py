from utils.token import get_user, authenticate_token
from fastapi import Depends, HTTPException, APIRouter
from typing import Dict
from database.models import User,Portfolio, ShoppingList, ShoppingTransaction
from database.hash import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from database.schemas import  ShoppingListCreateRequest, ShoppingListResponse, ShoppingTransactionCreateRequest, ShoppingTransactionResponse


router = APIRouter(prefix='/budget',
                   tags=['budget'])

@router.post("/create_shopping_list", response_model = ShoppingListResponse,
                                    description='Creat a shopping list')
async def create_shopping_list(new_shopping_list: ShoppingListCreateRequest,user: User = Depends(authenticate_token)):
    
        create_shopping_list = await ShoppingList.create(user=user, item=new_shopping_list.item, price = new_shopping_list.price, completed = new_shopping_list.completed
                                        
                                                    )

        response = ShoppingListResponse(user=user.username, item=new_shopping_list.item, price = new_shopping_list.price, completed = new_shopping_list.completed)
        return response



@router.post("/shopping_budget", response_model=ShoppingTransactionResponse,
                                description='Purchase items from the list with an ID and stay within budget')
async def shopping_budget(shopping_list_id: int, user: User = Depends(authenticate_token)):
    
        portfolio = await Portfolio.filter(user=user).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found.")
        
        shopping_list = await ShoppingList.get_or_none(id=shopping_list_id)
        if not shopping_list:
            raise HTTPException(status_code=404, detail="Shopping list not found.")
        
        budget_limit = portfolio.account_total * 0.8
        
        shopping_prices = await ShoppingList.filter(id=shopping_list_id).values_list('price', flat=True)
        total_shopping_price = sum(shopping_prices)
        
        if total_shopping_price > budget_limit:
            raise HTTPException(status_code=400, detail="Budget Exceeded")
        
        new_account_total = portfolio.account_total - total_shopping_price
        portfolio.account_total = new_account_total
        await portfolio.save()
        
        transaction = ShoppingTransaction(
            user=user,
            shoppinglist=shopping_list,
            amount=total_shopping_price
        )
        await transaction.save()
        
        response = ShoppingTransactionResponse(
            user=user.username,
            total_shopping_price=total_shopping_price
        )

        return response