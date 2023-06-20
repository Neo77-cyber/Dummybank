from tortoise import fields
from tortoise.models import Model
from database.hash import password_context




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