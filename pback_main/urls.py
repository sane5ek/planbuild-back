from django.urls import path
from django.contrib.auth.views import logout_then_login

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'pback_main'

urlpatterns = [
    path('upload', upload, name='upload'),
    path('subjects', subjects, name='subjects'),
    path('plan', plan, name='plan'),
    path('again', again, name='again')
]
