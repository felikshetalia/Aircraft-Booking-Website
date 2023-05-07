from django.urls import path
from . import views
from .views import  PlanesView

urlpatterns = [
    path('', views.my_view, name='my_view'),
    path('engineer/', views.EngineerDashboard, name='engineer'),
    path('planes/',PlanesView.as_view(),name='planes'),
    path('book_aircraft/', views.book_aircraft, name='book_aircraft'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/', views.book_aircraft_api, name='book_aircraft_api'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]

