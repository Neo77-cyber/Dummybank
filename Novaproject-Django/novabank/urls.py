from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name = 'register'),
    path('signin/', views.signin, name='signin'),
    path('logout', views.logout, name = 'logout'),
    path('create-profile/', views.createprofile, name='createprofile'),
    path('profile/', views.profile, name='profile'),
    path('portfolio/', views.portfolio, name = 'portfolio'),
    path('update-income/', views.updatebalance, name = 'updatebalance'),   
    path('transfer/', views.transfer, name = 'transfer'),
    path('shopping-list/', views.shoppinglist, name = 'shoppinglist'),
    path('del/<int:pk>/', views.deleteshoppingitem, name='deleteshoppingitem'),
    path('shop/<int:pk>/', views.shop, name='shop'),
    path('exchange-rate/', views.exchange_rates, name ='exchangerate'),
    path('FAQ', views.FAQ, name='FAQ'),
      
]
