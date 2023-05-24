from django.contrib import admin
from .models import Portfolio, Transactions, ShoppingList, ShoppingTransaction

# Register your models here.

admin.site.register(Portfolio)
admin.site.register(Transactions)
admin.site.register(ShoppingList)
admin.site.register(ShoppingTransaction)




