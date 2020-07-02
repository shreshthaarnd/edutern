from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse
import uuid
from app.myutil import *
import csv
from datetime import date

def check_user(request):
    try:
        uid=request.session['userid']
        return True
    except:
        return False
def get_user_courses(request):
    user_id=request.session['userid']
    course_ids=[]
    UserCourses.objects.filter(UserID=user_id).values('Course_ID').all()
    course=UserCourses.objects.filter(UserID=user_id).values('Course_ID').all()
    for i in course:
        course_ids.append(i['Course_ID'])
    course_data=[]
    for i in course_ids:
        a=CourseData.objects.filter(Course_ID=i)
        course_data.append(a)
    #print(course_data)
    data=[]
    for i in course_data:
        data.append(i[0])
    return data
	