from django.urls import re_path, path
from microsoft_authentication.views import (
    microsoft_login,
    microsoft_logout,
    callback,
    home
)

app_name = 'microsoft_authentication'
urlpatterns = [
    path('', home, name='home'),
    path('microsoft_authentication/login', microsoft_login, name="microsoft_authentication_login"),
    path('microsoft_authentication/logout', microsoft_logout, name="microsoft_authentication_logout"),
    path('microsoft_authentication/callback', callback, name="microsoft_authentication_callback"),
]