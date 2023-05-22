from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import  auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Transactions
import requests
from .forms import TransactionsForm, UserForm, PortfolioUpdateForm, CreateProfileForm
from django.contrib import messages
from django.db.models import Sum
from django.db import IntegrityError

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

def createprofile(request):
    createprofile_form = CreateProfileForm()
    if request.method == 'POST':
            createprofile_form = CreateProfileForm(request.POST, request.FILES)
            if createprofile_form.is_valid():
                try:
                    new_profile = createprofile_form.save(commit=False)
                    new_profile.username = request.user
                    new_profile.save()
                    createprofile_form = CreateProfileForm()
                    return render(request, 'createprofile.html')
                except IntegrityError:
                    error_message = "A profile already exists for this user."
                return render(request, 'createprofile.html', {'createprofileform': createprofile_form, 'error_message': error_message})


    return render (request, 'createprofile.html', {'createprofileform': createprofile_form})



@login_required(login_url='home')
def portfolio(request):
        log_user = request.user       
        try:
            portfolio = Portfolio.objects.filter(username=log_user)
            account_total = Portfolio.objects.filter(username=log_user).values()[0]['account_total']

            portfolio_instance = Portfolio.objects.get(username=log_user)

            amount_to_transfer = Transactions.objects.filter(username = portfolio_instance).values_list('amount_to_transfer', flat=True).order_by('-transaction_date')
        
        except Portfolio.DoesNotExist:
            portfolio = None
            account_total = 0    

        return render(request, 'portfolio.html', {'portfolio': portfolio, 'account_total': account_total, 'amount_to_transfer': amount_to_transfer })




def updatebalance(request):
    log_user = request.user.id
    portfolio_instance, created = Portfolio.objects.get_or_create(username=log_user)

    if request.method == 'POST':
        update_pin_form = PortfolioUpdateForm(request.POST, instance=portfolio_instance)
        if update_pin_form.is_valid():
            update_pin_form.save()
            messages.success(request, 'PIN and balance updated successfully.')
            return redirect('portfolio')

    else:
        update_pin_form = PortfolioUpdateForm(instance=portfolio_instance)

    return render(request, 'updatebalance.html', {'update_pin_form': update_pin_form})




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
                    sender_portfolio = Portfolio.objects.get(username=log_user)
                    transaction.username = sender_portfolio
                    transaction.save()

                    receiver_username = form.cleaned_data.get('beneficiary_name')
                    try:
                        receiver_portfolio = Portfolio.objects.get(username__username=receiver_username)
                        receiver_portfolio.account_total += amount_to_transfer
                        receiver_portfolio.save()

                        sender_portfolio.account_total -= amount_to_transfer
                        sender_portfolio.save()

                        messages.success(request, 'Transaction successful!')  
                        return redirect('portfolio')
                    except Portfolio.DoesNotExist:
                        messages.error(request, 'Transaction failed. Beneficiary not found.')  
                else:
                    messages.error(request, 'Invalid PIN or insufficient funds.')
            except (UnboundLocalError, IndexError, KeyError) as e:
                messages.error(request, 'Error: {}'.format(str(e)))
                pin = None
    else:
        form = TransactionsForm()

    return render(request, 'transfer.html', {'form': form})

def incometracker(request):
    createprofile_form = CreateProfileForm()
    if request.method == 'POST':
            createprofile_form = CreateProfileForm(request.POST, request.FILES)
            if createprofile_form.is_valid():
        
                    new_profile = createprofile_form.save(commit=False)
                    new_profile.username = request.user
                    new_profile.save()
                    createprofile_form = CreateProfileForm()
                    return render(request, 'incometracker.html')
               

    return render (request, 'incometracker.html')




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

def register(request):
    form_name = UserForm()
    if request.method =="POST":
        form_name = UserForm(request.POST)
        if form_name.is_valid():
            form_name.save()
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Password not secure') 
            return redirect('register')
    else:
        context = {'form_name':form_name}
        
    return render(request, 'register.html', context )
        

def logout(request):
    auth.logout(request)
    return redirect('signin')







# portfolio_instance = Portfolio.objects.get(username=log_user)

        # Exclude transfer transactions made by the user
        # amount_to_transfer = Transactions.objects.filter(username=portfolio_instance).exclude(beneficiary_name=log_user)

        # total_transfers = amount_to_transfer.aggregate(sum=Sum('amount_to_transfer'))
        # sum_transfers = total_transfers['sum']

        # if sum_transfers is not None:
        #     balance = portfolio_instance.account_total - sum_transfers
        # else:
        #     balance = portfolio_instance.account_total


#   balance': balance, 'amount_to_transfer': amount_to_transfe