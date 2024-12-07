from django.contrib import admin
from django.urls import re_path
from .views import *

admin.autodiscover()
app_name = 'accounts'


urlpatterns = [
    re_path(r'^register/$',UserRegister.as_view(),name="user_register_api"),
    re_path(r'^login/$',UserLogin.as_view(),name="user_login_api"),
]