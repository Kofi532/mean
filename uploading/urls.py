from django.urls import path

from . import views

app_name = "uploading"

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch/', views.fetch, name='fetch'),
    path('login/', views.login, name='logout'),
    path('deletestd/', views.delete_std, name='deletestd'),
    path('loggin/', views.loggin, name='loggin'),
]