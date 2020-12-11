from django.urls import path
from RealtimeAPS import views

app_name = 'RealtimeAPS'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('users/', views.users, name = 'users'),
    path('users/add/', views.user_add, name = 'user_add'),
    path('users/<int:pk>/', views.user_detail, name = 'user_detail'),
    path('projects/', views.projects, name = 'projects'),
    path('projects/add/', views.project_add, name = 'project_add'),
    path('projects/<int:pk>/', views.project_detail, name = 'project_detail'),
    path('projects/<int:pk>/user_add/', views.project_user_add, name = 'assign'),
    path('projects/<int:pk>/sensor_add/', views.project_sensor_add, name = 'sensor_add'),
]
