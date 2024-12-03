from django.urls import path
from.import views

app_name='Tour'

urlpatterns=[

    path('contact/',views.Contact,name='contact'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('booking/create/', views.create_booking, name='user_booking_create'),
    path('create-booking/<int:tour_id>/', views.create_booking, name='create_booking'),
    path('booking_success/', views.booking_success, name='booking_success'),

    #path('tour/<int:pk>/', views.user_tour_detail, name='tour_detail')
    #path('bookings/', views.user_booking_list, name='user_booking_list'),
    #path('bookings/create/', views.user_booking_create, name='user_booking_create'),
    #path('bookings/<int:pk>/update/', views.user_booking_update, name='user_booking_update'),
    #path('bookings/<int:pk>/delete/', views.user_booking_delete, name='user_booking_delete'),

]