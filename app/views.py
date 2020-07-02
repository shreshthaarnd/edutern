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
from .myutil import *

# Create your views here.
def logout(request):
	try:
		del request.session['userid']
		request.session.flush()
		return redirect('/index/')
	except:
		return redirect('/index/')
def socialreg(request):
	return render(request,'socialreg.html',{})
def index(request):
	dic={'checksession':check_user(request)}
	return render(request,'index.html',dic)
def aboutus(request):
	return render(request,'about-us.html',{})
def blog(request):
	return render(request,'blog.html',{})
def contact(request):
	return render(request,'contact.html',{})
def coursedetails(request):
	course_id=request.GET.get('course_id')
	user_id=request.session['userid']
	dic={'checksession':check_user(request)}
	if CourseData.objects.filter(Course_ID=course_id).exists():
		course_data=CourseData.objects.filter(Course_ID=course_id)
		lecture_data=LecturesData.objects.filter(Course_ID=course_id).all()
		if  UserCourses.objects.filter(UserID_id=user_id,Course_ID=course_id).exists():
			#status=UserCourses.objects.filter(UserID_id=user_id,Course_ID=course_id).values('status')[0]['status']
			status=True
		else:
			status=False
			
		return render(request,'course-details.html',{'dic':dic,'course_data':course_data,'lecture_data':lecture_data,'status':status})
	else:
		return HttpResponse("<h1>Course not found")
def courses(request):
	data=CourseData.objects.all()
	dic={'checksession':check_user(request)}
	return render(request,'courses.html',{'data':data, 'checksession':check_user})
def mycourses(request):
	'''user_id=request.session['userid']
	course_ids=[]
	UserCourses.objects.filter(UserID=user_id).values('Course_ID').all()
	course=UserCourses.objects.filter(UserID=user_id).values('Course_ID').all()
	for i in course:
		course_ids.append(i['Course_ID'])
	course_data=[]
	for i in course_ids:
		a=CourseData.objects.filter(Course_ID=i)
		course_data.append(a)
	print(course_data)
	data=[]
	for i in course_data:
		data.append(i[0])
	print(data)'''
	data=get_user_courses(request)
	return render(request,'courses.html',{'data':data,'checksession':check_user(request)})


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
def socialsave(request):
	if request.method=='POST':
		username=request.POST.get('username')
		email=request.POST.get('email')
		u="U00"
		x=1
		uid=u+str(x)
		while UserData.objects.filter(User_ID=uid).exists():
			x=x+1
			uid=u+str(x)
		x=int(x)
		obj=UserData(
			User_ID=uid,
			User_FName=username,
			User_Email=email
			)
		if UserData.objects.filter(User_Email=email):
			for x in UserData.objects.filter(User_Email=email):
				request.session['userid'] = x.User_ID
				break
			return redirect('/userdashboard/')
		else:
			obj.save()
			request.session['userid'] = uid
			return redirect('/userdashboard/')
@csrf_exempt
def saveuser(request):
	if request.method=='POST':
		fname=request.POST.get('fname')
		lname=request.POST.get('lname')
		email=request.POST.get('email')
		mobile=request.POST.get('mobile')
		password=request.POST.get('password')
		obj=UserData.objects.all().delete()
		u="U00"
		x=1
		uid=u+str(x)
		while UserData.objects.filter(User_ID=uid).exists():
			x=x+1
			uid=u+str(x)
		x=int(x)
		otp=uuid.uuid5(uuid.NAMESPACE_DNS, date.today().strftime("%d/%m/%Y")+uid+fname+lname+password+mobile+email).int
		otp=str(otp)
		otp=otp.upper()[0:6]
		request.session['userotp'] = otp
		obj=UserData(
			Join_Date=date.today().strftime("%d/%m/%Y"),
			User_ID=uid,
			User_FName=fname,
			User_LName=lname,
			User_Email=email,
			User_Phone=mobile,
			User_Password=password
			)
		if UserData.objects.filter(User_Email=email).exists():
			return HttpResponse("<script>alert('User Already Exists'); window.location.replace('/registration/')</script>")
		else:
			obj.save()
			msg='''Hi there!
Please verify your account with the following One Time Password

Verification OTP : '''+otp+'''

Thanks for creating your account on Edutern,
Team Edutern'''
			sub='Edutern One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[email])
			email.send()
			return render(request,'verify.html',{'userid':uid})
@csrf_exempt
def verifyuser(request):
	if request.method=='POST':
		otp=request.POST.get('otp')
		uid=request.POST.get('uid')
		if request.session['userotp'] == otp:
			request.session['userid'] = uid
			return HttpResponse("<script>alert('Account Created Successfully!'); window.location.replace('/userdashboard/')</script>")
		else:
			dic={'msg':'Incorrect OTP', 'userid':uid}
			return render(request,'verify.html',dic)
	else:
		return HttpResponse('<h1>400 Page Not Found</h1>')
def resendotp(request):
	uid=request.GET.get('uid')
	otp=request.session['userotp']
	email=''
	for x in UserData.objects.filter(User_ID=uid):
		email=x.User_Email
	msg='''Hi there!
Please verify your account with the following One Time Password

Verification OTP : '''+otp+'''

Thanks for creating your account on Edutern,
Team Edutern'''
	sub='Edutern One Time Password (OTP)'
	email=EmailMessage(sub,msg,to=[email])
	email.send()
	dic={'msg':'OTP Sent', 'userid':uid}
	return render(request,'verify.html',dic)
@csrf_exempt
def checklogin(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if UserData.objects.filter(User_Email=email,User_Password=password).exists():
			for x in UserData.objects.filter(User_Email=email,User_Password=password):
				request.session['userid']=x.User_ID
			return redirect('/userdashboard/')
		else:
			return HttpResponse("<script>alert('Incorrect Credentials'); window.location.replace('/login/')</script>")


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
	if check_user:
		uid=request.session['userid']
		data=UserData.objects.filter(User_ID=uid).all()
		my_courses=get_user_courses(request)
		course_id=[]
		lecture_id={}
		for i in my_courses:
			course_id.append(i.Course_ID)
		for i in course_id:
			lec_id=LecturesData.objects.filter(Course_ID=i).values('Lecture_ID')[0]['Lecture_ID']
			lecture_id[i]=lec_id
		print(lecture_id)



	return render(request,'userdashboard.html',{'data':data,'my_courses':my_courses,'lecture_id':lecture_id})
def courseplayer(request):
	uid=request.session['userid']
	lecture_id=request.GET.get('lecture_id')
	course_id=request.GET.get('course_id')
	print(uid)
	print(course_id)
	print(lecture_id)

	'''print(uid)
	#status=UserCourses.objects.filter(UserID=uid,Course_ID=course_id).values('status')[0]['status']
	#print(status)'''
	if UserCourses.objects.filter(UserID=uid,Course_ID=course_id,status=True).exists():
		lecture_data=LecturesData.objects.filter(Lecture_ID=lecture_id)
		lecture_list=LecturesData.objects.filter(Course_ID=course_id).all()
		return render(request,'courseplayer.html',{'lecture_data':lecture_data,'lecture_list':lecture_list})
	else:
		return HttpResponse("<script>alert('Please enroll into the course'); window.location.replace('/courses/')</script>")
	
	

def adminaddlectures(request):
	try:
		adminid=request.session['adminid']
		data=CourseData.objects.all()
		return render(request,'adminpages/addlectures.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
@csrf_exempt
def adminsavelecture(request):
	if request.method=='POST':
		course=request.POST.get('course')
		name=request.POST.get('name')
		video=request.FILES['video']
		l="LEC00"
		x=1
		lid=l+str(x)
		while LecturesData.objects.filter(Lecture_ID=lid).exists():
			x=x+1
			lid=l+str(x)
		x=int(x)
		obj=LecturesData(
			Lecture_ID=lid,
			Course_ID=course,
			Lecture_Name=name,
			Lecture_Video=video
			)
		obj.save()
		return HttpResponse("<script>alert('Lecture Added Successfully'); window.location.replace('/adminaddlectures/')</script>")
	else:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminlectureslist(request):
	try:
		adminid=request.session['adminid']
		data=LecturesData.objects.all()
		return render(request,'adminpages/lectureslist.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminuserslist(request):
	return render(request,'adminpages/userslist.html',{})
def adminactiveusers(request):
	return render(request,'adminpages/activeusers.html',{})
def admindeactiveusers(request):
	return render(request,'adminpages/deactiveusers.html',{})

def admincourseenrolls(request):
	return render(request,'adminpages/courseenrolls.html',{})
def admincoursespayment(request):
	return render(request,'adminpages/coursespayment.html',{})
def adminuserreview(request):
	return render(request,'adminpages/userreview.html',{})

def forget_password(request):
	if request.method=='POST':
		uid=request.session['userid']
		password=''
		data=UserData.objects.filter(User_ID=uid)
		for x in data:
			password=x.User_Password
		sub='Edutern - Your Account Password'
		email=request.POST['email']
		msg='''Hi there!
Your Edutern Account Password is,

'''+password+'''

Thanks for creating your account on Edutern,
Team Edutern'''
		email=EmailMessage(sub,data,to=[email])
		email.send()
		return HttpResponse("<script>alert('Your Password has been send to your mail'); window.location.replace('/login/')</script>")
	else:
		return render(request,'forgot_password.html',{})
def editUserDetail(request):
	if request.method=='POST':
		uid=request.session['userid']
		user_data=UserData.objects.filter(User_ID=uid)
		for i in user_data:
			i.User_FName=request.POST['first_name']
			i.User_LName=request.POST['last_name']
			i.User_Phone=request.POST['phone']
			i.save()
			return HttpResponse("<script>alert('Congratulations !! Your details is SuccessFully Updated'); window.location.replace('/userdashboard/')</script>")
def editPassword(request):
	if request.method=='POST':
		uid=request.session['userid']
		user_data=UserData.objects.filter(User_ID=uid)
		old_pass=UserData.objects.filter(User_ID=uid).values('User_Password')[0]['User_Password']
		old_password=request.POST['old_password']
		if old_pass==old_password:
			for i in user_data:
				new_pass=int(request.POST['new_password'])
				i.User_Password=new_pass
				i.save()
				return HttpResponse("<script>alert('Congratulations !! Your Password is SuccessFully Updated'); window.location.replace('/userdashboard/')</script>")
		else:
			return HttpResponse("<script>alert('Pleasr check your old password'); window.location.replace('/userdashboard/')</script>")
def checkout(request):
	if request.method=='POST':
		course_id=request.GET.get('course_id')
		user_id=request.session['userid']
		#userid=UserData.objects.filter(User_ID=user_id).values('id')[0]['id']
		print(user_id)
		#print(userid)
		#ur_id=UserData.objects.filter(User_ID=user_id).values('id')[0]['id']
		usercourse=UserCourses(UserID_id=user_id,Course_ID=course_id,status=True)
		usercourse.save()
		return HttpResponse("<script>alert('Congratulations !! Your course is SuccessFully Buyed'); window.location.replace('/userdashboard/')</script>")

	else:
		course_id=request.GET.get('course_id')
		course_data=CourseData.objects.filter(Course_ID=course_id)
		return render(request,'checkout.html',{'course_data':course_data,'checksession':check_user(request)})

def admincompletecourses(request):
	return render(request,'adminpages/completecourses.html',{})
def adminincompletecourses(request):
	return render(request,'adminpages/incompletecourses.html',{})