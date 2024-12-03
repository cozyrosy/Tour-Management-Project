
from django import forms
from .models import Booking, Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour_date', 'num_of_people']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
