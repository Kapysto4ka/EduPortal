from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'students'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/<str:name>', views.menu, name='menu'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/cancel_submission/', views.cancel_submission, name='cancel_submission'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)