from django.urls import path
from django.contrib.auth.views import logout_then_login

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'pback_interaction'

urlpatterns = [
    path('search', search, name='search'),
    path('adopt', adopt, name='adopt'),
    path('request', request, name='request'),

    path('accept', accept, name='accept'),
    path('decline', decline, name='decline'),
    path('cancel', cancel, name='cancel'),
]
