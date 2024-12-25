from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='homepage'),
    path('products/', products_list, name='products'),
    path('product/<str:slug>/', product_detail, name='product-detail'),
    path('auth/status/', account_status, name="is_authenticated"),
]
