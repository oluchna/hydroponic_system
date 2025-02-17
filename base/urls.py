from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', views.LoginView.as_view(), name='login'), 
    path('systems/', views.HydroponicSystemView.as_view(), name='systems'), 
    path('sensors/', views.SensorReadingView.as_view(), name='sensors'), 
    path('systems/<uuid:pk>/', views.HydroponicSystemEdit.as_view(), name='hydroponic-system-edit')
]