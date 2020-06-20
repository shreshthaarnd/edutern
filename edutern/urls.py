from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index),
    path('aboutus/',aboutus),
    path('blog/',blog),
    path('contact/',contact),
    path('coursedetails/',coursedetails),
    path('courses/',courses),
    path('elements/',elements),
    path('singleblog/',singleblog),
    path('adminindex/',adminindex),
    path('adminlogin/',adminlogin),
    path('admincodorderlist/',admincodorderlist),
    path('login/',login),
    path('registration/',registration),
]
