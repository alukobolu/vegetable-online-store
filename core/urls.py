from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/<int:id>/', cart_add, name='cart_add'),
    path('cart-remove/<int:id>/', cart_remove, name='cart_remove'),
    path('cart-update/<int:id>/', cart_updated, name='cart_updated'), 
    path('cartt', CartTemplate.as_view(), name='cart'),
    path('contact', Contact.as_view(), name='contact'),
    path('checkout',Checkout.as_view(),name="checkout"),
] 
