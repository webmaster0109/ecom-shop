from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User


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

def register_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse({'status' : 'success', 'message': 'Already Logged In'})
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not first_name or not last_name or not email or not password or not confirm_password:
            return JsonResponse({'status' : 'error', 'message': 'All fields are required'}, status=400)
        
        if password != confirm_password:
            if [first_name, last_name, email] in password:
                return JsonResponse({'status' : 'error', 'message': 'Password must not contain name or email'}, status=400)
            return JsonResponse({'status' : 'error', 'message': 'Passwords do not match'}, status=400)
        
        if Profile.objects.filter(user__email=email).exists():
            return JsonResponse({'status' : 'error', 'message': 'Email is already exists'}, status=400)
        
        
        user_obj = User(
                    username=str(email).split('@')[0], 
                    email=email, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name)
        user_obj.set_password(password)
        user_obj.save()
        profile_obj = Profile(user=user_obj)
        profile_obj.is_verified = True
        profile_obj.save()
        login(request, user_obj)
        return JsonResponse({'status' : 'success', 'message': 'Account created successfully'}, status=200)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, template_name='auth/register.html')

def logout_user(request):
    logout(request)
    return redirect('login-page')