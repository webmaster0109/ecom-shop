from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse


def login_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, template_name='auth/login.html')

def login_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse({'status' : 'success', 'message': 'Already Logged In'})
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)

        if not username or not password:
            return JsonResponse({'status' : 'error', 'message': 'All fields are required'}, status=400)
        
        user_obj = authenticate(request, username=username, password=password)

        if user_obj:
            user = Profile.objects.get(user=user_obj)
            if not user.is_verified:
                return JsonResponse({'status' : 'error', 'message': 'Account is not verified'}, status=400)
            login(request, user_obj)
            return JsonResponse({'status' : 'success', 'message': 'Login Successful'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message': 'Invalid Credentials'}, status=401)
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def logout_user(request):
    logout(request)
    return redirect('login-page')