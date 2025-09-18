from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

# Personal Itinerary Models
class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itineraries")
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Hotel(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name="hotels")
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    check_in = models.DateField()
    check_out = models.DateField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.name} ({self.itinerary.name})"

class Activity(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name="activities")
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.itinerary.name})"
from django.db import models
from django.contrib.auth.models import User

# Transport options for Destinations
class Transport(models.Model):
    city = models.CharField(max_length=100, default="Unknown")  # Instead of ForeignKey to Destination
    vehicle_name = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.vehicle_name} ({self.city})"

# Destination Model
class Destination(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destinations", null=True, blank=True)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


# User Profile with Location
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Reviews for Destinations
class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=5)  # 1–5 scale
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
class TouristPlace(models.Model):

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='images/default.jpg', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_places', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
