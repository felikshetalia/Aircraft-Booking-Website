from django.urls import path
from .views import SignUpView, EngineerView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('engineer/', EngineerView.as_view(), name='signup'),
   
]
