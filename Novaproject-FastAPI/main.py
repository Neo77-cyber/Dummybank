from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers import users, profile, transaction, budget
from database.models import Portfolio, Transaction, ShoppingList, ShoppingTransaction





app = FastAPI(
    description = 'A Finance management app that allows users manage their finances, The API initiates transactions, create shopping lists and set up a budget plan to improve spending habits'
)
app.include_router(users.router)
app.include_router(profile.router)
app.include_router(transaction.router)
app.include_router(budget.router)



register_tortoise(
    app,
    db_url='sqlite:///Users/neo/Documents/Codez/projectz/novaprojectz/Novaproject-FastAPI/database.db',
    modules={'models': ['database.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)







       



    




    




