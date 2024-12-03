from django.urls import path
from . import views

app_name = 'Manager'

urlpatterns = [

    path('', views.manager_home, name='home'),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tours/<int:tour_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('tours/<int:tour_id>/review/', views.create_review, name='create_review'),

]
