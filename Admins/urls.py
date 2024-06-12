from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('AdminPanel/login', views.admin_panel_login, name='AdminPanel'),
]
