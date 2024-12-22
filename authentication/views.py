from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
import uuid
from mails.forgot_send_mail import send_forgot_mail
from django.contrib.auth.hashers import check_password


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

def forgot_password_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, template_name='auth/forgot_password.html')

def forgot_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)
            user_obj = User.objects.filter(email=email).first()
            if not user_obj:
                return JsonResponse({'status': 'error', 'message': 'User not found. Register Now!'}, status=401)
            
            profile_obj = Profile.objects.get(user=user_obj)
            if not profile_obj.is_verified:
                return JsonResponse({'status': 'error', 'message': 'Account is not verified. Please verify the account first'}, status=400)
            
            last_time_sent = profile_obj.modified_at
            if last_time_sent and (timezone.now() - last_time_sent) < timedelta(minutes=10) and profile_obj.forgot_password_token != None:
                time_difference = (timezone.now() - last_time_sent)
                time_left = timedelta(minutes=10) - time_difference
                if time_left.seconds > 60:
                    return JsonResponse({'status': 'error', 'message': f'Please wait for {time_left.seconds//60} minutes before sending another email'}, status=400)
            
            token = str(uuid.uuid4())
            profile_obj.forgot_password_token = token
            profile_obj.modified_at = timezone.now()
            profile_obj.save()
            send_forgot_mail(request, profile_obj, token)
            return JsonResponse({'status': 'success', 'message': 'Password reset successfully'}, status=200)
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def check_password_similiarity(new_password, old_password):
    common_password = set(new_password) & set(old_password)
    similiarity_percentage = (len(common_password) / len(new_password)) * 100
    print(similiarity_percentage)
    return similiarity_percentage <= 60


def reset_password_page(request, token):
    profile_obj = Profile.objects.filter(forgot_password_token=token).first()
    if not profile_obj:
        JsonResponse({'status': 'error', 'message': 'Invalid token, request new one.'}, status=400)
        return redirect('login-page')
    return render(request, template_name='auth/reset_password.html', 
                  context={'token': profile_obj.forgot_password_token, 'user_id': profile_obj.user.id})

def reset_password(request, token):
    try:
        profile_obj = Profile.objects.filter(forgot_password_token=token).first()
        if not profile_obj:
            return JsonResponse({'status': 'error', 'message': 'Invalid token, request new one.'}, status=400)
        if profile_obj and profile_obj.modified_at + timedelta(minutes=10) < timezone.now():
            profile_obj.forgot_password_token = None
            profile_obj.save()
            return JsonResponse({'status': 'error', 'message': 'Password reset link expired, request new one.'}, status=400)
        
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                return JsonResponse({'status': 'error', 'message': 'No User Id Found.'}, status=400)
            if not password or not confirm_password:
                return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)
            if password != confirm_password:
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=400)
            
            user_obj = User.objects.filter(id=user_id).first()
            
            if check_password(password, user_obj.password):
                return JsonResponse({'status': 'error', 'message': 'Password cannot be same as old password'}, status=400)
            
            if check_password_similiarity(password, user_obj.password):
                print(check_password_similiarity(password, user_obj.password))
                return JsonResponse({'status': 'error', 'message': 'Password is too similiar to old password'}, status=400)
            

            user_obj.set_password(password)
            user_obj.save()
            profile_obj.forgot_password_token = None
            profile_obj.modified_at = timezone.now()
            profile_obj.save()
            return JsonResponse({'status': 'success', 'message': 'Password reset successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)