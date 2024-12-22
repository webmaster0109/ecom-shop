from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def index(request):
    url = request.META.get('REMOTE_ADDR')
    print(url)
    return render(request, template_name='index.html')