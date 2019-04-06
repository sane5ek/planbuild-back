from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('pback_auth.urls')),
    path('api/main/', include('pback_main.urls')),
    path('api/settings/', include('pback_settings.urls')),
    path('api/interaction/', include('pback_interaction.urls')),
]
