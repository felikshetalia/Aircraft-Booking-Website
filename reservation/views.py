from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Aircraft, Booking, Review
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.contrib import messages

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.db.models import Q
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
logger = logging.getLogger(__name__)


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
    query = request.GET.get('q', '')
    aircraft_type = request.GET.get('type', '')
    origin = request.GET.get('origin', '')

    filters = Q()

    if query:
        filters &= Q(model__icontains=query)

    if aircraft_type:
        filters &= Q(model__icontains=aircraft_type)

    if origin:
        filters &= Q(country__icontains=origin)

    filters &= ~Q(timeForInspection__lte=datetime.today())
    aircrafts = Aircraft.objects.filter(filters)
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

        # Check if the aircraft is available
        if not aircraft.availability:
            return render(request, 'book_aircraft.html', {'error': 'Aircraft is not available for booking'})

        booking = Booking.objects.create(aircraft=aircraft, user=request.user, start_time=start_time, end_time=end_time, status='Pending')
        aircraft.availability = False
        aircraft.save()
        return render(request, 'booking_confirmation.html', {'booking': booking})
    else:
        aircrafts = Aircraft.objects.filter(availability=True)
        models = Aircraft.objects.values_list('model', flat=True).distinct()
        return render(request, 'book_aircraft.html', {'models': models})

@login_required
def plane_details(request, aircraft_id):
    try:
        aircraft = Aircraft.objects.get(id=aircraft_id)
    except Aircraft.DoesNotExist:
        return render(request, 'home.html', {'error_message': 'Aircraft not found'})

    return render(request, 'aircraft_detail.html', {'aircraft': aircraft})

def booking_confirmation(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return render(request, 'book_aircraft.html', {'error': 'Booking not found'})

    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def booking_list(request):
    print("Accessing booking_list")
    check_completed_bookings()

    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

def check_completed_bookings():
    print("Checking status")
    current_time = timezone.now()
    print(current_time)
    bookings = Booking.objects.filter(status='Pending', end_time__lte=current_time)
    for booking in bookings:
        booking.status = 'Completed'
        booking.save()


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


def about(request):
    return render(request, 'About.html', {'title': 'About'})


def contact(request):
    return render(request, 'Contact.html', {'title': 'contact'})

def review(request):
    return render(request, 'review.html', {'title': 'review'})

@csrf_exempt
@login_required
def add_review(request, aircraft_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        comment = data.get('comment')
        rating = data.get('rating')
        name = data.get('name')
        email = data.get('email')

        if comment and rating and name and email:
            aircraft = get_object_or_404(Aircraft, id=aircraft_id)

            Review.objects.create(user=request.user, aircraft=aircraft, comment=comment, rating=int(rating))
            messages.success(request, "Your review has been submitted successfully")

            # Since this is an API now, we need to return JSON response
            return JsonResponse({'message': 'Review submitted successfully'})

        else:
            print(comment)
            print(rating)
            print(name)
            print(email)
            return JsonResponse({'error': 'Please fill all the fields'}, status=400)

    elif request.method == 'GET':
        booking = get_object_or_404(Booking, id=aircraft_id)
        return render(request, 'review.html', {'booking': booking})
    



def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if comment and rating:
            review.comment = comment
            review.rating = rating
            review.save()
            messages.success(request, "Your review has been updated successfully")

           #Darya says this need to be fixed
           # return redirect('review_confirmation')

    return render(request, 'edit_review.html', {'review': review})


