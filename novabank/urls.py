from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('signin/', views.signin, name='signin'),
    path('transfer/', views.transfer, name = 'transfer'),
    path('logout', views.logout, name = 'logout'),
    path('portfolio/', views.portfolio, name = 'portfolio'),
    # path('test/', views.transfer_funds, name = 'test'),

    
    
]
