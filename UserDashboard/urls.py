from django.urls import path
from . import views

urlpatterns = [
    path('menu/<str:id>', views.projects_section_view, name='menu'),
    path("", views.index),
]