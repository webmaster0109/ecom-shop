from django.shortcuts import render
from rest_framework.generics import ListAPIView

from products.models import Product
from .serializers import ProductSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
