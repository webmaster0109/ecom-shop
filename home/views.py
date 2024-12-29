from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product
from django.core.serializers import serialize
import json

@login_required(login_url='/account/login/')
def index(request):
    url = request.META.get('REMOTE_ADDR')
    print(url)
    return render(request, template_name='index.html')

@login_required(login_url='/account/login/')
def products_list(request):
    products = Product.objects.all()
    products_serialized = serialize('json', products)
    products_data = json.loads(products_serialized)
    formatted_products = [
        {
            'id': product['pk'],
            'name': product['fields']['name'],
            'slug': product['fields']['slug'],
            'price': product['fields']['price'],
            'description': product['fields']['description'],
            'image': product['fields']['image'],
        }
        for product in products_data
    ]
    print({'status': 'success', 'products': formatted_products})
    return JsonResponse({'status': 'success', 'products': products_serialized}, safe=False)

@login_required(login_url='/account/login/')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, template_name='products/product_detail.html', context={'product':product})

def account_status(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'is_authenticated': is_authenticated})


# secret_key = QwSscc8Ecu02QbLgEfAffGI7AAX1APUv