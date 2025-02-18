from django.urls import path

from .views import auth, hydroponics, sensors


urlpatterns = [ 
    path('login/', auth.LoginView.as_view(), name='login'), 
    path('systems/', hydroponics.HydroponicSystemView.as_view(), name='systems'), 
    path('sensors/', sensors.SensorReadingView.as_view(), name='sensors'), 
    path('systems/<uuid:pk>/', hydroponics.HydroponicSystemEdit.as_view(), name='hydroponic-system-edit')
]