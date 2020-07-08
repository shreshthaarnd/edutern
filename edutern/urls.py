from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index),
    path('',index),
    path('aboutus/',aboutus),
    path('blog/',blog),
    path('contact/',contact),
    path('coursedetails/',coursedetails),
    path('courses/',courses),
    path('elements/',elements),
    path('singleblog/',singleblog),
    path('saveuser/',saveuser),
    path('resendotp/',resendotp),
    path('verify/',verifyuser),
    path('checklogin/',checklogin),
    path('userdashboard/',userdashboard),
    path('courseplayer/',courseplayer),
    path('openlecture/',openlecture),
    path('accounts/', include('allauth.urls')),
    path('socialreg/', socialreg),
    path('socialsave/', socialsave),
    path('logout/', logout),
    path('downloadcert/', downloadcert),
    path('admindeleteenrolls/', admindeleteenrolls),
    path('adminlogout/', adminlogout),

    path('adminindex/',adminindex),
    path('adminlogin/',adminlogin),
    path('admincodorderlist/',admincodorderlist),
    path('adminlogincheck/',adminlogincheck),
    path('adminaddcourse/',adminaddcourse),
    path('adminsavecourse/',adminsavecourse),
    path('admincourselist/',admincourselist),
    path('adminaddlectures/',adminaddlectures),
    path('adminsavelecture/',adminsavelecture),
    path('adminlectureslist/',adminlectureslist),
    path('adminuserslist/',adminuserslist),
    path('adminactiveusers/',adminactiveusers),
    path('makeuserdeactive/',makeuserdeactive),
    path('admindeactiveusers/',admindeactiveusers),
    path('makeuseractive/',makeuseractive),
    path('admincourseenrolls/',admincourseenrolls),
    path('admincoursespayment/',admincoursespayment),
    path('adminuserreview/',adminuserreview),
    path('deletereview/',deletereview),
    path('admincompletecourses/',admincompletecourses),
    path('adminincompletecourses/',adminincompletecourses),
    
    path('login/',login),
    path('registration/',registration),
    path('forget_password/',forget_password),
    path('editUserDetail/',editUserDetail),
    path('editPassword/',editPassword),
    path('checkout/',checkout),
    path('mycourses/',mycourses),
    path('reviewform/',reviewform),
    path('adminsendcertificate/',adminsendcertificate),
    path('adminsendbulk/',adminsendbulk),
    path('adminsendtoone/',adminsendtoone),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)