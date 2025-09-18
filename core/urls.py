from django.urls import path
from django.conf.urls.static import static
from travel_duide_project import settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tourist-places/", views.tourist_place, name="tourist_places"),
    path("tourist-place/<int:pk>/", views.tourist_place_detail, name="tourist_place_detail"),
    path("tourist-place/<int:parent_pk>/add-sub-place/", views.add_sub_tourist_place, name="add_sub_tourist_place"),
    path("destination/<int:pk>/", views.destination_detail, name="destination_detail"),
    path("login/", views.login_view, name="login"),
    path("register/", views.registration_view, name="registration"),
    path("logout/", views.logout_view, name="logout"),
    path("set-location/", views.set_location, name="set_location"),
    path("add-destination/", views.add_destination, name="add_destination"),
    path("destination/<int:pk>/delete/", views.delete_destination, 
         name="delete_destination"),
    # Itinerary URLs
    path("itineraries/", views.itinerary_list, name="itinerary_list"),
    path("itineraries/add/", views.itinerary_create, name="itinerary_create"),
    path("itineraries/<int:pk>/", views.itinerary_detail, name="itinerary_detail"),
    path("itineraries/<int:itinerary_pk>/add-hotel/", views.hotel_add, name="hotel_add"),
    path("itineraries/<int:itinerary_pk>/add-activity/", views.activity_add, name="activity_add"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)