from django.urls import path
from .views import *

urlpatterns = [
    path('products/', productsView),
    path('products/<int:pk>/', productView),
    path('login/', login),
    path('register/', registration),
    path('cart/', cartInfo),
    path('cart/<int:pk>/', cartChange)
]