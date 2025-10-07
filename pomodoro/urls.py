from django.urls import path
from . import views

urlpatterns = [
    path('', views.pomodoro_timer, name='pomodoro_timer'),
    path('start/', views.start_timer, name='start_timer'),
    path('pause/', views.pause_timer, name='pause_timer'),
    path('resume/', views.resume_timer, name='resume_timer'),
    path('stop/', views.stop_timer, name='stop_timer'),
    path('update-session-name/', views.update_session_name, name='update_session_name'),
    path('update-log-name/', views.update_log_name, name='update_log_name'),
    path('status/', views.get_timer_status, name='get_timer_status'),
]
