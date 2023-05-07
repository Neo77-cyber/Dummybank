from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Portfolio(models.Model):
    username= models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=500, blank= True, null = True)
    last_name = models.CharField(max_length=200, blank= True, null = True)
    city = models.CharField(max_length=200, blank= True, null = True)
    Country = models.CharField(max_length=200, blank= True, null = True)
    state = models.CharField(max_length=200, blank= True, null = True)
    address = models.CharField(max_length=200, blank= True, null = True)
    phone_number = models.IntegerField( blank= True, null = True)
    zipcode = models.IntegerField( blank= True, null = True)
    profile_image = models.ImageField(blank=True, null=True, upload_to="images/")
    account_total = models.IntegerField(blank= True, null = True)
    pin = models.IntegerField(null= True, blank= True)

    def __str__(self):
        return self.first_name 
    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
class Transactions(models.Model):
    username = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, blank= True, null = True)
    beneficiary_name = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    branch_name = models.CharField(max_length=200)
    bank_address = models.CharField(max_length=200)
    account_number = models.IntegerField()
    account_type = models.CharField(max_length=200)
    amount_to_transfer = models.IntegerField()
    beneficiary_email = models.EmailField(max_length=200)
    beneficiary_phone_number = models.IntegerField()
    bank_swift_code = models.IntegerField()
    transfer_pin = models.IntegerField(null=True, blank=True)
    transaction_date = models.DateField(default=timezone.now)
    

    def __str__(self):
        return self.beneficiary_name
    


    



    