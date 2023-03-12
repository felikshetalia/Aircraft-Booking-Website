from django.http import HttpResponse

def my_view(request):
    return HttpResponse("<html><body><h1>Hello, world!</h1></body></html>")
