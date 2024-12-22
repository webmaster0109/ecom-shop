from django.urls import path
from .views import *

urlpatterns = [
    path('login-attempt/', login_user, name='user-login'),
    path('login/', login_page, name='login-page'),
    path('logout/', logout_user, name='auth-logout'),
]
