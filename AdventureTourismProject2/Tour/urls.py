from django.urls import path
from . import views
from .views import *


app_name='Tour'

urlpatterns=[

    path('contact/',views.Contact,name='contact'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    # path('booking/create/', views.create_booking, name='user_booking_create'),
    path('new_booking/<int:tour_id>/', views.new_booking, name='new_booking'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('user_bookings/', views.user_bookings, name='user_bookings'),

    #path('tour/<int:pk>/', views.user_tour_detail, name='tour_detail')
    #path('bookings/', views.user_booking_list, name='user_booking_list'),
    #path('bookings/create/', views.user_booking_create, name='user_booking_create'),
    #path('bookings/<int:pk>/update/', views.user_booking_update, name='user_booking_update'),

    path('blogs/', views.blogs, name='blogs'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),

]