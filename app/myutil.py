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
        progress=int((watched_lecture/total_lectures)*100)
    return progress

def downloaddata(table):
    if table=='CourseData':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=CourseData.csv'
        writer = csv.writer(response)
        writer.writerow(["Course_ID", "Course_Name", "Course_Trainer", "Course_Fee", "Course_Objective", "Course_Eligibility", "Course_Thumb"])
        obj1=CourseData.objects.all()
        for X in obj1:
            writer.writerow([X.Course_ID, X.Course_Name, X.Course_Trainer, X.Course_Fee, X.Course_Objective, X.Course_Eligibility, X.Course_Thumb])
        return response
    if table=='LecturesData':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=LecturesData.csv'
        writer = csv.writer(response)
        writer.writerow(["Lecture_ID", "Course_ID", "Lecture_Name", "Lecture_Video"])
        obj1=LecturesData.objects.all()
        for x in obj1:
            writer.writerow([x.Lecture_ID, x.Course_ID, x.Lecture_Name, x.Lecture_Video])
        return response
    if table=='UserData':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=UserData.csv'
        writer = csv.writer(response)
        writer.writerow(["Join_Date", "User_ID", "User_FName", "User_LName", "User_Email", "User_Phone", "User_Password", "Verify_Status", "Status"])
        obj1=UserData.objects.all()
        for x in obj1:
            writer.writerow([x.Join_Date, x.User_ID, x.User_FName, x.User_LName, x.User_Email, x.User_Phone, x.User_Password, x.Verify_Status, x.Status])
        return response
    if table=='UserCourses':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=UserCourses.csv'
        writer = csv.writer(response)
        writer.writerow(["Pay_ID", "Coupon", "UserID", "Course_ID", "status"])
        obj1=UserCourses.objects.all()
        for x in obj1:
            writer.writerow([x.Pay_ID, x.Coupon, x.UserID, x.Course_ID, x.status])
        return response
    if table=='UserReviews':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=UserReviews.csv'
        writer = csv.writer(response)
        writer.writerow(["Review_ID", "User_ID", "User_Name", "Course_ID", "Review", "Feedback"])
        obj1=UserReviews.objects.all()
        for x in obj1:
            writer.writerow([x.Review_ID, x.User_ID, x.User_Name, x.Course_ID, x.Review, x.Feedback])
        return response
    if table=='UserLectures':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=UserLectures.csv'
        writer = csv.writer(response)
        writer.writerow(["User_ID", "Course_ID", "Lecture_ID", "Lecture_Watched"])
        obj1=UserLectures.objects.all()
        for x in obj1:
            writer.writerow([x.User_ID, x.Course_ID, x.Lecture_ID, x.Lecture_Watched])
        return response
    if table=='CertificatesData':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=CertificatesData.csv'
        writer = csv.writer(response)
        writer.writerow(["Cert_ID", "Certificate"])
        obj1=CertificatesData.objects.all()
        for x in obj1:
            writer.writerow([x.Cert_ID, x.Certificate])
        return response
    if table=='CouponData':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=CouponData.csv'
        writer = csv.writer(response)
        writer.writerow(["Coupon_ID", "Coupon_Name", "Coupon_Code", "Coupon_Code", "Discount"])
        obj1=CouponData.objects.all()
        for x in obj1:
            writer.writerow([x.Coupon_ID, x.Coupon_Name, x.Coupon_Code, x.Coupon_Code, x.Discount])
        return response
    if table=='PaymentData':
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment;filename=PaymentData.csv'
        writer = csv.writer(response)
        writer.writerow(["Pay_ID", "CURRENCY", "GATEWAYNAME", "RESPMSG", "BANKNAME", "PAYMENTMODE", "RESPCODE", "TXNID", "TXNAMOUNT", "STATUS", "BANKTXNID", "TXNDATE", "CHECKSUMHASH"])
        obj1=PaymentData.objects.all()
        for x in obj1:
            writer.writerow([x.Pay_ID, x.CURRENCY, x.GATEWAYNAME, x.RESPMSG, x.BANKNAME, x.PAYMENTMODE, x.RESPCODE, x.TXNID, x.TXNAMOUNT, x.STATUS, x.BANKTXNID, x.TXNDATE, x.CHECKSUMHASH])
        return response