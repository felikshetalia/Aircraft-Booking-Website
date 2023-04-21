from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic



class PlanesView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('planes')
    template_name = 'planes/planeslist.html'

def my_view(request):
    return HttpResponse("<html><body><h1>Hello, world!</h1></body></html>")



