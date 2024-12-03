from django.urls import path
from.import views

app_name='user'

urlpatterns=[
    path('home/', views.home, name='home'),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('login/user/profile/',views.Customer_Profile,name='profile'),
]






