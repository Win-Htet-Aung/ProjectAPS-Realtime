from django.urls import path
from DataManagement import views

app_name = 'DataManagement'

urlpatterns = [
    path('', views.index, name = 'data'),
]
