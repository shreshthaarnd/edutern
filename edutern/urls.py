from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

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
    path('userdashboard/',userdashboard),
    path('courseplayer/',courseplayer),

    path('adminindex/',adminindex),
    path('adminlogin/',adminlogin),
    path('admincodorderlist/',admincodorderlist),
    path('adminlogincheck/',adminlogincheck),
    path('adminaddcourse/',adminaddcourse),
    path('adminsavecourse/',adminsavecourse),
    path('admincourselist/',admincourselist),
    
    path('login/',login),
    path('registration/',registration),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)