from django.db import models
from django.contrib.auth.models import User
from Manager.models import Tour

# Create your models here.


class UserBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    date = models.DateField()
    num_people = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')])

    def __str__(self):
        return f'{self.user.username} - {self.tour.title} on {self.date}'

    def calculate_total_price(self):
        return self.num_people * self.tour.price

    def save(self, *args, **kwargs):
        # Calculate total_price before saving
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super(UserBooking, self).save(*args, **kwargs)
