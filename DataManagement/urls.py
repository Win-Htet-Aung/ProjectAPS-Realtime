from django.urls import path
from DataManagement import views

app_name = 'DataManagement'

urlpatterns = [
    path('', views.index, name = 'data'),
    path('upload/', views.data_upload, name = 'upload'),
    path('<str:proj>/<str:serial>/', views.data_get, name = 'data_get'),
]
