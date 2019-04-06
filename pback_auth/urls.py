from django.urls import path
from django.contrib.auth.views import logout_then_login

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'pback_auth'

urlpatterns = [
    path('token', obtain_auth_token, name='api_token_auth'),
    path('register', register, name='register')
]
