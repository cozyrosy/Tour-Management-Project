from django.contrib import admin
from .models import UserBooking



class UserBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'date', 'status')  # Use 'date' instead of 'tour_date'
    list_filter = ('date', 'status')  # Use 'date' instead of 'tour_date'
    search_fields = ('user__username', 'tour__title')  # Enable search functionality

admin.site.register(UserBooking, UserBookingAdmin)
