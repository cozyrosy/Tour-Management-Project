from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Tour(models.Model):
    LOCATION_CHOICES = [
        ('Manali', 'Manali'),
        ('Goa', 'Goa'),
        ('Jaipur', 'Jaipur'),
        ('Leh', 'Leh'),
        ('Rishikesh', 'Rishikesh'),
        ('Kerala', 'Kerala'),
        ('Andaman', 'Andaman'),
        ('Darjeeling', 'Darjeeling'),
        ('Shimla', 'Shimla'),
        ('Varanasi', 'Varanasi'),
    ]

    ADVENTURE_CHOICES = [
        ('Hiking', 'Hiking'),
        ('Scuba Diving', 'Scuba Diving'),
        ('Safari', 'Safari'),
        ('Skydiving', 'Skydiving'),
        ('Camping', 'Camping'),
        ('City Tour', 'City Tour'),
        ('Rafting', 'Rafting'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    adventure_type = models.CharField(max_length=100, choices=ADVENTURE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    max_group_size = models.PositiveIntegerField()
    itinerary = models.TextField(blank=True)
    image = models.ImageField(upload_to='tours/images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.adventure_type} in {self.location}"



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    tour_date = models.DateField()
    num_of_people = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.tour.title} on {self.tour_date}"

    def save(self, *args, **kwargs):
        self.total_price = self.num_of_people * self.tour.price
        super().save(*args, **kwargs)


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 rating
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.tour.title} - {self.rating} Stars"


class Blog(models.Model):
    """
    Basic model to store blog posts.
    """
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/manager/', blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    author_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


