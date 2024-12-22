from django.urls import path
from .views import *

urlpatterns = [
    path('login-attempt/', login_user, name='user-login'),
    path('login/', login_page, name='login-page'),
    path('register/', register_page, name='register-page'),
    path('register-attempt/', register_user, name='user-register'),
    path('logout/', logout_user, name='auth-logout'),
    path('forgot-password-attempt/', forgot_password, name='forgot-password'),
    path('forgot-password/', forgot_password_page, name='forgot-password-page'),
    path('reset-password/<token>', reset_password_page, name='reset-password-page'),
    path('reset-password-attempt/<token>/', reset_password, name='reset-password'),
]
