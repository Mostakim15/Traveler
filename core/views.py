import math

from urllib3 import request
# ------------------------
# Distance Calculation Helper
# ------------------------


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.conf.urls.static import static
from django.conf import settings

from .models import (
    Destination, UserProfile, Review, Transport, TouristPlace,
    Itinerary, Hotel, Activity
)
from django.db.models import Q
from .forms_itinerary import ItineraryForm, HotelForm, ActivityForm
from .forms import DestinationForm  # Make sure your DestinationForm is in forms.py


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the Earth (haversine formula)."""
    if None in (lat1, lon1, lat2, lon2):
        return None
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return round(distance, 2)
# Detail view for a single TouristPlace
def tourist_place_detail(request, pk):
    place = get_object_or_404(TouristPlace, pk=pk)
    sub_places = place.sub_places.all()
    return render(request, "tourist_place_detail.html", {"place": place, "sub_places": sub_places})
def add_sub_tourist_place(request, parent_pk):
    parent = get_object_or_404(TouristPlace, pk=parent_pk)
    if request.method == "POST":
        name = request.POST.get("name")
        country = request.POST.get("country")
        city = request.POST.get("city")
        description = request.POST.get("description")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        image = request.FILES.get("image")
        sub_place = TouristPlace.objects.create(
            name=name,
            country=country,
            city=city,
            description=description,
            latitude=latitude,
            longitude=longitude,
            image=image,
            parent=parent
        )
        messages.success(request, "Sub tourist place added successfully.")
        return redirect("tourist_place_detail", pk=parent_pk)
    return render(request, "add_sub_tourist_place.html", {"parent": parent})


from django.utils.translation import gettext as _
# ------------------------
# Home Page
# ------------------------
def home(request):
    destinations = Destination.objects.all()
    query = request.GET.get('search', '')
    if query:
        tourist_places = TouristPlace.objects.filter(name__icontains=query)
    else:
        tourist_places = TouristPlace.objects.all()
    return render(request, "home.html", {"destinations": destinations, "tourist_places": tourist_places, "search_query": query})


# ------------------------
# Tourist Places
# ------------------------
def tourist_place(request):
    places = TouristPlace.objects.all()
    return render(request, "touristP.html", {"places": places})


# ------------------------
# Destination Details + Reviews
# ------------------------
def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    transports = Transport.objects.filter(city=destination.city) if destination.city else []
    reviews = destination.reviews.all()

    # Calculate distance from user profile to destination
    distance = None
    dynamic_transports = []
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            if profile.latitude is not None and profile.longitude is not None:
                distance = calculate_distance(
                    profile.latitude, profile.longitude,
                    destination.latitude, destination.longitude
                )
                # Calculate dynamic fare for each transport
                for t in transports:
                    # Example: dynamic fare = base fare * (distance + 1)
                    try:
                        fare = float(t.fare) * (distance + 1) if distance is not None else float(t.fare)
                    except Exception:
                        fare = t.fare
                    dynamic_transports.append({
                        'vehicle_name': t.vehicle_name,
                        'dynamic_fare': fare,
                        'base_fare': t.fare,
                    })
            else:
                for t in transports:
                    dynamic_transports.append({
                        'vehicle_name': t.vehicle_name,
                        'dynamic_fare': t.fare,
                        'base_fare': t.fare,
                    })
        except UserProfile.DoesNotExist:
            for t in transports:
                dynamic_transports.append({
                    'vehicle_name': t.vehicle_name,
                    'dynamic_fare': t.fare,
                    'base_fare': t.fare,
                })
    else:
        for t in transports:
            dynamic_transports.append({
                'vehicle_name': t.vehicle_name,
                'dynamic_fare': t.fare,
                'base_fare': t.fare,
            })

    if request.method == "POST" and request.user.is_authenticated:
        comment = request.POST.get("comment")
        rating = int(request.POST.get("rating", 5))
        Review.objects.create(destination=destination, user=request.user, comment=comment, rating=rating)
        messages.success(request, "Review added successfully.")
        return redirect("destination_detail", pk=pk)

    # Find hotels in this destination's city or with address/name matching destination
    if destination.city:
        hotels = Hotel.objects.filter(
            Q(address__icontains=destination.city) |
            Q(itinerary__name__icontains=destination.city) |
            Q(itinerary__name__icontains=destination.name)
        )
    else:
        hotels = Hotel.objects.filter(itinerary__name__icontains=destination.name)
    from django.conf import settings
    return render(request, "destination_detail.html", {
        "destination": destination,
        "reviews": reviews,
        "transports": dynamic_transports,
        "distance": distance,
        "hotels": hotels,
        "GOOGLE_MAPS_API_KEY": getattr(settings, "GOOGLE_MAPS_API_KEY", "")
    })


# ------------------------
# Login / Registration / Logout
# ------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "registration.html")


def registration_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("registration")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("registration")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "User created successfully.")
        return redirect("home")

    return render(request, "registration.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------------
# Set Location
# ------------------------
@login_required
def set_location(request):
    if request.method == "POST":
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.latitude = lat
        profile.longitude = lon
        profile.save()
        messages.success(request, "Location saved successfully.")
        return redirect("home")
    return render(request, "set_location.html")


# ------------------------
# Destination CRUD
# ------------------------
@login_required
def add_destination(request):
    if request.method == "POST":
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user
            destination.save()
            messages.success(request, "Destination added successfully.")
            return redirect("home")
    else:
        form = DestinationForm()
    return render(request, "add_destination.html", {"form": form})


@login_required
def delete_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        destination.delete()
        messages.success(request, "Destination deleted successfully.")
        return redirect("home")
    return render(request, "confirm_delete.html", {"destination": destination})


# ------------------------
# Itinerary CRUD
# ------------------------
@login_required
def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, "itinerary_list.html", {"itineraries": itineraries})


@login_required
def itinerary_create(request):
    if request.method == "POST":
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.save()
            messages.success(request, "Itinerary created!")
            return redirect("itinerary_list")
    else:
        form = ItineraryForm()
    return render(request, "itinerary_form.html", {"form": form})


@login_required
def itinerary_detail(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    hotels = itinerary.hotels.all()
    activities = itinerary.activities.all()
    return render(request, "itinerary_detail.html", {
        "itinerary": itinerary,
        "hotels": hotels,
        "activities": activities
    })


@login_required
def hotel_add(request, itinerary_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.itinerary = itinerary
            hotel.save()
            messages.success(request, "Hotel added!")
            return redirect("itinerary_detail", pk=itinerary_pk)
    else:
        form = HotelForm()
    return render(request, "hotel_form.html", {"form": form, "itinerary": itinerary})


@login_required
def activity_add(request, itinerary_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.itinerary = itinerary
            activity.save()
            messages.success(request, "Activity added!")
            return redirect("itinerary_detail", pk=itinerary_pk)
    else:
        form = ActivityForm()
    return render(request, "activity_form.html", {"form": form, "itinerary": itinerary})

