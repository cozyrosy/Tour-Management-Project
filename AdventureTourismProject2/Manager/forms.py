
from django import forms
from .models import Booking, Blog, Review, Tour
from Tour.models import UserBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = UserBooking
        fields = ['date', 'num_people', 'status']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CreateTourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'location', 'adventure_type', 'price', 'start_date',
                  'end_date', 'max_group_size', 'itinerary', 'image']

