from pydantic import BaseModel




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

class ShoppingTransactionCreateRequest(BaseModel):
    amount: int
    shopping_list_id: int  

class ShoppingTransactionResponse(BaseModel):
    user: str
    total_shopping_price: float