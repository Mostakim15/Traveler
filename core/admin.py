from django.contrib import admin
from .models import Destination, UserProfile, Review, Transport, TouristPlace

admin.site.register(Destination)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Transport)
admin.site.register(TouristPlace)
