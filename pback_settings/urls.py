from django.urls import path
from django.contrib.auth.views import logout_then_login

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'pback_settings'

urlpatterns = [
    path('info', info, name='info'),
    path('user', user, name='user'),
    path('edit', edit, name='edit'),
    path('email', email, name='email'),
    path('password', password, name='password'),

    path('fields', fields, name='fields'),
    path('default', default, name='default'),
    path('owner', owner, name='owner'),
    path('save', save, name='save'),
]
