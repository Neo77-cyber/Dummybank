from database.schemas import PortfolioResponse,PortfolioCreateRequest
from utils.token import get_user, authenticate_token
from fastapi import Depends, HTTPException, APIRouter
from typing import Dict
from database.models import User,Portfolio
from database.hash import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from database.schemas import PortfolioResponse,PortfolioCreateRequest



router = APIRouter(prefix='/profile',
                   tags=['Profile'])


@router.post("/create_profile", response_model = PortfolioResponse,
             description= 'Create a user profile')
async def create_profile(new_profile:PortfolioCreateRequest, user: User = Depends(authenticate_token)):

            create_profile = await Portfolio.create(user=user, account_total=new_profile.account_total, pin = new_profile.pin                               
                                                    )

            response = PortfolioResponse(user=user.username, account_total = new_profile.account_total, pin = new_profile.pin )
            return response


@router.get("/portfolio", response_model=PortfolioResponse,
                        description='Retrieve the current user profile')
async def portfolio(user: User = Depends(authenticate_token)):
        
        portfolio = await Portfolio.filter(user=user).first()

        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        response = PortfolioResponse(
            user=user.username,
            account_total=portfolio.account_total,
            pin=portfolio.pin
        )

        return response

    
@router.put("/update_portfolio", response_model=PortfolioResponse,
                                description='Update the current user profile')
async def portfolio(update_portfolio:PortfolioCreateRequest, user: User = Depends(authenticate_token)):
    
        portfolio = await Portfolio.filter(user=user).first()

        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found.")
        await Portfolio.filter(id=portfolio.id).update(account_total=update_portfolio.account_total, pin=update_portfolio.pin)

        response = PortfolioResponse(user=user.username, account_total=update_portfolio.account_total, pin=update_portfolio.pin)

        return response