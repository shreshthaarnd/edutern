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
	
def get_Course_Rating(request):
    data=CourseData.objects.all()
    sum=0
    course_rating={}
    for i in data:
        sum=0
        if UserReviews.objects.filter(Course_ID=i.Course_ID).exists():
            rating=UserReviews.objects.filter(Course_ID=i.Course_ID).all()
            for j in rating:
                sum=sum+int(j.Review)
            count=UserReviews.objects.filter(Course_ID=i.Course_ID).count()
            average_rating=sum/count
        else:
            average_rating=0
        course_rating[i.Course_ID]=average_rating
    return course_rating
def get_Progress(request,course_id):
    progress=0
    if 	UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id).exists():
        total_lectures=UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id).count()
        watched_lecture=UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id,Lecture_Watched=True).count()
        progress=(watched_lecture/total_lectures)*100
    return progress