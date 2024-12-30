from django.urls import path
from .views import *

urlpatterns = [
    path('products-list/', ProductListView.as_view(), name='products-list'),
]
