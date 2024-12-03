from django import forms
from .models import UserBooking
import datetime



class UserBookingForm(forms.ModelForm):
    class Meta:
        model = UserBooking
        fields = ['tour', 'date', 'num_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'num_people': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'tour': 'Tour',
            'date': 'Date',
            'num_people': 'Number of People',
        }

   # Ensure this import is at the top of your file

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date <= datetime.date.today():
            raise forms.ValidationError("The booking date must be in the future.")
        return date
