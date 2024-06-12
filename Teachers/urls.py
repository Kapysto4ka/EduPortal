from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_dashboard, name='dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/attendance/', views.attendance_overview, name='attendance_overview'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('menu/<str:name>/', views.menu, name='menu'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('attendance_overview/<int:group_id>/', views.attendance_overview, name='attendance_overview'),
    path('add_attendance/', views.add_attendance, name='add_attendance'),
    #path('create_subject/', views.create_subject, name='create_subject'),
    path('view_grades/<int:group_id>/', views.view_grades, name='view_grades'),
    path('create_assignment/<int:group_id>/', views.create_assignment, name='create_assignment'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('assignment/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)