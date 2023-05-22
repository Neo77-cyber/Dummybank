from django import forms
from .models import Transactions, Portfolio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('first_name', 'last_name', 'city', 'Country', 'state', 'address', 'phone_number', 'zipcode', 'profile_image', 'account_total', 'pin' )


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('beneficiary_name', 'bank_name', 'branch_name', 'bank_address', 'account_number', 'account_type', 'amount_to_transfer', 'beneficiary_email', 'beneficiary_phone_number', 'bank_swift_code', 'transfer_pin' ) 

class PortfolioUpdateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['pin', 'account_total']

