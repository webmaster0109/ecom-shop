from django.urls import path
from .views import *

urlpatterns = [
    path('login-attempt/', login_user, name='user-login'),
    path('login/', login_page, name='login-page'),
    path('register/', register_page, name='register-page'),
    path('register-attempt/', register_user, name='user-register'),
    path('logout/', logout_user, name='auth-logout'),
]
