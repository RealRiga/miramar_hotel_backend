from django.contrib import admin
from .models import User, Room, Booking, Feedback, Offer, UserProfile

# admin.site.register(User)
admin.site.register(UserProfile)
# admin.site.register(Room)
# admin.site.register(Booking)
# admin.site.register(Feedback)
# admin.site.register(Offer)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('destTitle', 'price', 'availability')
    search_fields = ('destTitle',)
    list_filter = ('availability',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'approved')
    search_fields = ('user__username', 'room__destTitle')
    list_filter = ('approved', 'check_in', 'check_out')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'discount')
    search_fields = ('title', 'location')
    list_filter = ('price', 'discount')
