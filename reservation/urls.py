from django.urls import path
from . import views
from .views import  PlanesView

urlpatterns = [
    path('', views.my_view, name='my_view'),
     path('planes/',PlanesView.as_view(),name='planes')
]
