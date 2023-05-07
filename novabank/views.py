from django.shortcuts import render, redirect
from django.contrib.auth.models import  auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Transactions
import requests
from .forms import TransactionsForm
from django.contrib import messages
from django.db.models import Sum

# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

# def get_exchange_rates():
    # endpoint = "https://v6.exchangerate-api.com/v6/9633a5f18ca5b8ccc65aaa80/latest/NGN"
    # response = requests.get(endpoint)
    # data = response.json()
    # return data['conversion_rates']


@login_required(login_url='home')
def transfer(request):
    log_user = request.user.id

    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        if form.is_valid():
            try:
                pin = int(form.cleaned_data.get('transfer_pin'))
                saved_pin = Portfolio.objects.filter(username=log_user).values()[0]['pin']
                amount_to_transfer = int(form.cleaned_data.get('amount_to_transfer'))
                account_total = Portfolio.objects.filter(username=log_user).values()[0]['account_total']

                if pin == saved_pin and amount_to_transfer <= account_total:
                    transaction = form.save(commit=False)
                    transaction.username = Portfolio.objects.get(username=log_user)
                    transaction.save()
                    messages.success(request, 'Transaction successful!')
                    return redirect('portfolio')

                elif amount_to_transfer > account_total:
                    messages.error(request, 'Insufficient funds')

                else:
                    messages.error(request, 'Account suspended. Your request to transfer funds has been declined. Contact support for help ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌')
            except UnboundLocalError:
                pin = None
    else:
        form = TransactionsForm()

    return render(request, 'transfer.html', {'form': form})


@login_required(login_url='home')
def portfolio(request):
    log_user = request.user

    portfolio_instance = Portfolio.objects.get(username=log_user)
    
    portfolio = Portfolio.objects.filter(username=log_user)

    account_total = Portfolio.objects.filter(username =log_user ).values()[0]['account_total']

    amount_to_transfer = Transactions.objects.filter(username = portfolio_instance).values_list('amount_to_transfer', flat=True).order_by('-transaction_date')

    total_transfers = amount_to_transfer.aggregate(Sum('amount_to_transfer'))
    
    sum_transfers = total_transfers['amount_to_transfer__sum']
    if sum_transfers is not None:
        balance = account_total - sum_transfers
    else:
        balance = account_total

    return render(request, 'portfolio.html', {'portfolio': portfolio, 'balance': balance, 'amount_to_transfer': amount_to_transfer})





###############################      LOGIN    #################################

def signin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username = username, password= password)

            if user is not None:
                auth.login(request,user)
                return redirect('portfolio')
            else:
                messages.info(request, 'Enter a valid User ID')
                return redirect('signin')
        return render(request, 'signin.html')
        

def logout(request):
    auth.logout(request)
    return redirect('signin')





