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

    # URLs for the users CRUDs
    path('users_list/', views.users_list, name='users_list'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),

    path('tours/<int:tour_id>/review/', views.create_review, name='create_review'),

    # URLs for the blog CRUDs
    path('blog_list/', views.blog_list, name='blog_list'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('edit_blog/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:pk>/', views.delete_blog, name='delete_blog'),

]
