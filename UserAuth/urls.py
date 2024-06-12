from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
] 