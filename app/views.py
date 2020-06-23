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

# Create your views here.
def index(request):
	return render(request,'index.html',{})
def aboutus(request):
	return render(request,'about-us.html',{})
def blog(request):
	return render(request,'blog.html',{})
def contact(request):
	return render(request,'contact.html',{})
def coursedetails(request):
	return render(request,'course-details.html',{})
def courses(request):
	return render(request,'courses.html',{})
def elements(request):
	return render(request,'elements.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def admincodorderlist(request):
	return render(request,'adminpages/codorderlist.html',{})
def login(request):
	return render(request,'login.html',{})
def registration(request):
	return render(request,'registration.html',{})

@csrf_exempt
def adminlogincheck(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if email == 'admin@edutern.in' and password == '1234':
			request.session['adminid'] = email
			return redirect('/adminindex/')
		else:
			return HttpResponse("<script>alert('Incorrect Credentials'); window.location.replace('/adminlogin/')</script>")
	else:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminindex(request):
	try:
		adminid=request.session['adminid']
		return render(request,'adminpages/index.html',{})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminaddcourse(request):
	try:
		adminid=request.session['adminid']
		return render(request,'adminpages/addcourse.html',{})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
@csrf_exempt
def adminsavecourse(request):
	try:
		adminid=request.session['adminid']
		if request.method=='POST':
			name=request.POST.get('name')
			trainer=request.POST.get('trainer')
			fee=request.POST.get('fee')
			objective=request.POST.get('objective')
			eligibility=request.POST.get('eligibility')
			contents=request.POST.get('content')
			thumbnail=request.FILES['thumbnail']
			c="CRS00"
			x=1
			cid=c+str(x)
			while CourseData.objects.filter(Course_ID=cid).exists():
				x=x+1
				cid=c+str(x)
			x=int(x)
			obj=CourseData(
				Course_ID=cid,
				Course_Name=name,
				Course_Trainer=trainer,
				Course_Fee=fee,
				Course_Objective=objective,
				Course_Eligibility=eligibility,
				Course_Content=contents,
				Course_Thumb=thumbnail
				)
			if CourseData.objects.filter(Course_Name=name).exists():
				return HttpResponse("<script>alert('Course Already Exists'); window.location.replace('/adminaddcourse/')</script>")
			else:
				obj.save()
				return HttpResponse("<script>alert('Course Added Successfully'); window.location.replace('/adminaddcourse/')</script>")
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admincourselist(request):
	try:
		adminid=request.session['adminid']
		dic={'data':CourseData.objects.all()}
		return render(request,'adminpages/courselist.html',dic)
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def userdashboard(request):
	return render(request,'userdashboard.html',{})