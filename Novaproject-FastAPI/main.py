from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from datetime import datetime
from typing import Dict









app = FastAPI()

SECRET_KEY = "FMe1o0baNLQ_ntPVuK2FTGWwxc_m1KfuKWp0xgReaJg"

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

password_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")   


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length = 100)
    password_hash = fields.CharField(max_length = 100)
    

    async def verify_password(self, plain_password):
        return password_context.hash(plain_password)
    
    class PydanticMeta:
        exclude = ["password_hash"]

class Portfolio(Model):
    user = fields.OneToOneField("models.User", on_delete=fields.CASCADE, related_name="portfolio")
    account_total= fields.IntField()
    pin = fields.IntField()
    
class Transaction(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    beneficiary_name = fields.CharField(max_length=200)
    amount_to_transfer = fields.IntField()
    transfer_pin = fields.IntField()
    
class ShoppingList(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    item = fields.CharField(max_length=200)
    price = fields.IntField()
    completed = fields.BooleanField()

class ShoppingTransaction(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="shopping_transactions")
    shoppinglist = fields.ForeignKeyField("models.ShoppingList", related_name="transactions")
    amount = fields.IntField()

    class Meta:
        table = "shopping_transaction"

class PortfolioCreateRequest(BaseModel):
    account_total: int
    pin: int
    
class PortfolioResponse(BaseModel):
    user: str
    account_total: int
    pin: int

class TransactionCreateRequest(BaseModel):
    beneficiary_name: str
    amount_to_transfer: int
    transfer_pin: int

class TransactionResponse(BaseModel):
    user: str
    beneficiary_name: str
    amount_to_transfer: int
    transfer_pin: int

class ShoppingListCreateRequest(BaseModel):
    item: str
    price: int
    completed: bool

class ShoppingListResponse(BaseModel):
    user: str
    item: str
    price: int
    completed: bool

class ShoppingTransactionCreateResquest(BaseModel):
    amount: int
    shoppinglist_id: int

class ShoppingTransactionResponse(BaseModel):
    user: str
    shoppinglist_id: int
    




register_tortoise(
    app,
    db_url='sqlite:///Users/neo/Documents/Codez/FASTApipractice/financefastapi/database.db',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

async def get_user(username: str):
    return await User.get_or_none(username=username)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def authenticate_user(user:User, password: str):
    if not user or not verify_password(password, user.password_hash):
        return False
    else:
        return user
    
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/register')
async def register(username:str, password:str):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code = 400, detail = 'Username already exists')
    hashed_password = password_context.hash(password)
    user = await User.create(username=username, password_hash = hashed_password)
    return {"message": "Registered successfuly"}

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

    
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"message": "Protected route accessed successfully."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}




@app.post("/create_profile", response_model = PortfolioResponse )
async def create_profile(new_profile:PortfolioCreateRequest, token:str = Depends(oauth2_scheme)):
    try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            user = await get_user(username)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token.")
            create_profile = await Portfolio.create(user=user, account_total=new_profile.account_total, pin = new_profile.pin
                                        
                                                    )

            response = PortfolioResponse(user=user.username, account_total = new_profile.account_total, pin = new_profile.pin )
            return response

    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token.")

@app.get("/portfolio", response_model=PortfolioResponse)
async def portfolio(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

        portfolio = await Portfolio.filter(user=user).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        response = PortfolioResponse(
            user=user.username,
            account_total=portfolio.account_total,
            pin=portfolio.pin
        )
        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

@app.put("/update_portfolio", response_model=PortfolioResponse)
async def portfolio(update_portfolio:PortfolioCreateRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

        portfolio = await Portfolio.filter(user=user).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found.")
        await Portfolio.filter(id=portfolio.id).update(account_total=update_portfolio.account_total, pin=update_portfolio.pin)
        response = PortfolioResponse(user=user.username, account_total=update_portfolio.account_total, pin=update_portfolio.pin)
        return response
       

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


@app.post("/create_transaction", response_model=TransactionResponse)
async def create_transaction(new_transaction: TransactionCreateRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

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

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    

@app.post("/create_shopping_list", response_model = ShoppingListResponse)
async def create_shopping_list(new_shopping_list: ShoppingListCreateRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        create_shopping_list = await ShoppingList.create(user=user, item=new_shopping_list.item, price = new_shopping_list.price, completed = new_shopping_list.completed
                                        
                                                    )

        response = ShoppingListResponse(user=user.username, item=new_shopping_list.item, price = new_shopping_list.price, completed = new_shopping_list.completed)
        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    

@app.post("/shopping_budget", response_model=ShoppingTransactionResponse)
async def shopping_budget(
    shopping_list_id: int,
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
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

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")




    




