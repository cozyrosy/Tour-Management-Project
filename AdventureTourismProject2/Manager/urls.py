from django.urls import path
from . import views

app_name = 'Manager'

urlpatterns = [

    path('', views.manager_home, name='home'),

    # URLS for the tour CRUDs
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('create_tour/', views.create_tour, name='create_tour'),
    path('edit_tour/<int:pk>/', views.edit_tour, name='edit_tour'),
    path('delete_tour/<int:pk>/', views.delete_tour, name='delete_tour'),

    # URLS for the booking CRUDs
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('create_booking/<int:tour_id>/', views.create_booking, name='create_booking'),
    path('edit_booking/<int:pk>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:pk>/', views.delete_booking, name='delete_booking'),


    path('tours/<int:tour_id>/review/', views.create_review, name='create_review'),

]
