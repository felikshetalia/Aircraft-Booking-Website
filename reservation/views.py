from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Aircraft, Booking
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings


class PlanesView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('planes')
    template_name = 'planes/planeslist.html'

@login_required
def EngineerDashboard(request):
    if request.method == 'GET':
        aircrafts = Aircraft.objects.order_by('timeForInspection')
        booking = Booking.objects.all()
        return render(request,'engineer/engineer.html', {'aircrafts': aircrafts , "booking_list":booking })



def my_view(request):
    aircrafts = Aircraft.objects.all()
    context = {'aircrafts': aircrafts}
    return render(request, 'home.html', context)



@login_required
def book_aircraft(request):
    if request.method == 'POST':
        aircraft_id = request.POST.get('aircraft_id')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        if not (aircraft_id and start_time_str and end_time_str):
            return render(request, 'book_aircraft.html', {'error': 'Missing required fields'})
        
        try:
            start_time = parse_datetime(start_time_str)
            end_time = parse_datetime(end_time_str)
        except ValueError:
            return render(request, 'book_aircraft.html', {'error': 'Invalid datetime format'})
        
        if start_time >= end_time:
            return render(request, 'book_aircraft.html', {'error': 'End time must be after start time'})
        
        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
        except Aircraft.DoesNotExist:
            return render(request, 'book_aircraft.html', {'error': 'Aircraft not found'})
        
        if not aircraft.availability:
            return render(request, 'book_aircraft.html', {'error': 'Aircraft is not available for booking'})
        
        booking = Booking.objects.create(aircraft=aircraft, user=request.user, start_time=start_time, end_time=end_time, status='Pending')
        aircraft.availability = False
        aircraft.save()
        return render(request, 'booking_confirmation.html', {'booking': booking})
    else:
        aircrafts = Aircraft.objects.filter(availability=True)
        return render(request, 'book_aircraft.html', {'aircrafts': aircrafts})
    


def booking_confirmation(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return render(request, 'book_aircraft.html', {'error': 'Booking not found'})

    return render(request, 'booking_confirmation.html', {'booking': booking})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'booking_list.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user, status='Pending')
    except Booking.DoesNotExist:
        return redirect('booking_list')
    
    aircraft = booking.aircraft
    aircraft.availability = True
    aircraft.save()
    
    booking.status = 'Cancelled'
    booking.save()
    
    return redirect('booking_list')

@require_POST
@login_required
def book_aircraft_api(request):
    aircraft_id = request.POST.get('aircraftId')
    start_time_str = request.POST.get('bookingStartDateTime')




def about(request):
    return render(request, 'About.html', {'title': 'About'})


def contact(request):
    return render(request, 'Contact.html', {'title': 'contact'})