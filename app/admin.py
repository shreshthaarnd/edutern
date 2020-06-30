from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserData)
admin.site.register(CourseData)
admin.site.register(LecturesData)
admin.site.register(UserCourses)