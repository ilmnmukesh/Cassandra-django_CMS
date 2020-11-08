
from django.contrib import admin
from django.urls import path, include
from login.views import home

urlpatterns = [
    path('',home, name="home"),
    path('login/', include('login.urls')),
    path('signup/', include('signup.urls')),
    path('',include('editprofile.urls')),
    path('home/catering/',include('home_catering.urls')),
    path('home/catboy/',include('home_catboy.urls')),
    path('home/customer/', include('home_customer.urls')),
    path('home/mahal/', include('home_mahal.urls'))
]
