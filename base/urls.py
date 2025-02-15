from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test), 
    path('login/', views.LoginView.as_view(), name='login')
]
