from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('register/', views.register, name = 'register'),
    path('signin/', views.signin, name='signin'),
    path('logout', views.logout, name = 'logout'),
    path('createprofile/', views.createprofile, name='createprofile'),
    path('portfolio/', views.portfolio, name = 'portfolio'),
    path('updatebalance/', views.updatebalance, name = 'updatebalance'),   
    path('transfer/', views.transfer, name = 'transfer'),
    path('incometracker', views.incometracker, name = 'incometracker')
    
]
