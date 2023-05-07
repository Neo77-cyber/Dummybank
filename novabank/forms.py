from django import forms
from .models import Transactions


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('beneficiary_name', 'bank_name', 'branch_name', 'bank_address', 'account_number', 'account_type', 'amount_to_transfer', 'beneficiary_email', 'beneficiary_phone_number', 'bank_swift_code', 'transfer_pin' ) 