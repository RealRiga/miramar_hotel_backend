from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main.views import (
    user_login, user_register, fetch_offers, fetch_rooms, 
    user_details, CustomAuthToken, password_reset, password_reset_confirm, 
    search_rooms, view_rooms, book_room, check_booked_rooms, cancel_booked_room,
    update_profile, logout, submit_feedback
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', CustomAuthToken.as_view(), name='user_login'),
    path('api/register/', user_register, name='user_register'),
    path('api/password_reset/', password_reset, name='password_reset'),
    path('api/password_reset_confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('api/user/', user_details, name='user_details'),
    path('api/offers/', fetch_offers, name='fetch_offers'),
    path('api/rooms/', fetch_rooms, name='fetch_rooms'),
    path('api/search_rooms/', search_rooms, name='search_rooms'),
    path('api/view_rooms/', view_rooms, name='view_rooms'),
    path('api/book_room/', book_room, name='book_room'),
    path('api/check_booked_rooms/', check_booked_rooms, name='check_booked_rooms'),
    path('api/cancel_booked_room/<int:booking_id>/', cancel_booked_room, name='cancel_booked_room'),
    path('api/update_profile/', update_profile, name='update_profile'),
    path('api/book_room/', book_room, name='book_room'),
    path('api/feedback/', submit_feedback, name='submit_feedback'),
    path('api/logout/', logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
