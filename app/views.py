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
import os
from django.conf import settings
# Create your views here.
def logout(request):
	try:
		del request.session['userid']
		request.session.flush()
		return redirect('/index/')
	except:
		return redirect('/index/')
def socialreg(request):
	dic={'checksession':check_user(request)}
	return render(request,'socialreg.html',dic)
def index(request):
	dic={'checksession':check_user(request)}
	return render(request,'index.html',dic)
def aboutus(request):
	dic={'checksession':check_user(request)}
	return render(request,'about-us.html',dic)
def blog(request):
	dic={'checksession':check_user(request)}
	return render(request,'blog.html',dic)
def contact(request):
	dic={'checksession':check_user(request)}
	return render(request,'contact.html',dic)
def coursedetails(request):
	try:
		course_id=request.GET.get('course_id')
		user_id=request.session['userid']
		if CourseData.objects.filter(Course_ID=course_id).exists():
			course_data=CourseData.objects.filter(Course_ID=course_id)
			lecture_data=LecturesData.objects.filter(Course_ID=course_id).all()
			reviews=UserReviews.objects.filter(Course_ID=course_id).all()
			if  UserCourses.objects.filter(UserID_id=user_id,Course_ID=course_id,status=True).exists():
				status=True
				if not UserReviews.objects.filter(User_ID=user_id,Course_ID=course_id).exists():
					review_status=True
				else:
					review_status=False
				dic={'checksession':check_user(request),
					'course_data':course_data,
					'lecture_data':lecture_data,
					'status':status,
					'review_status':review_status,
					'reviews':reviews}			
				return render(request,'course-details.html',dic)		
			else:
				status=False
				review_status=False
				dic={'checksession':check_user(request),
					'course_data':course_data,
					'lecture_data':lecture_data,
					'status':status,
					'review_status':review_status,
					'reviews':reviews}
				return render(request,'course-details.html',dic)
		else:
			return HttpResponse("<h1>Course not found</h1>")
	except:
		course_id=request.GET.get('course_id')
		if CourseData.objects.filter(Course_ID=course_id).exists():
			course_data=CourseData.objects.filter(Course_ID=course_id)
			lecture_data=LecturesData.objects.filter(Course_ID=course_id).all()
			reviews=UserReviews.objects.filter(Course_ID=course_id).all()
			print('hello')
			dic={'checksession':check_user(request),
				'course_data':course_data,
				'lecture_data':lecture_data,
				'reviews':reviews}
			return render(request,'course-details.html',dic)
		else:
			return HttpResponse("<h1>Course not found</h1>")
	
def courses(request):
	data=CourseData.objects.all()
	dic={'checksession':check_user(request)}
	course_rating=get_Course_Rating(request)
	print(course_rating)
	return render(request,'courses.html',{'data':data, 'checksession':check_user,'course_rating':course_rating})
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
	dic={'checksession':check_user(request)}
	return render(request,'single-blog.html',dic)
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def admincodorderlist(request):
	return render(request,'adminpages/codorderlist.html',{})
def login(request):
	dic={'checksession':check_user(request)}
	return render(request,'login.html',dic)
def registration(request):
	dic={'checksession':check_user(request)}
	return render(request,'registration.html',dic)
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
def reviewform(request):
	if request.method=='POST':
		userid=request.session['userid']
		user_fname=UserData.objects.filter(User_ID=userid).values('User_FName')[0]['User_FName']
		user_lname=UserData.objects.filter(User_ID=userid).values('User_LName')[0]['User_LName']
		review=request.POST['star']
		feedback=request.POST['feedback']
		Course_id=request.GET.get('course_id')
		user_name=user_fname+" "+user_lname
		r="REV00"
		x=1
		rid=r+str(x)
		while UserReviews.objects.filter(Review_ID=rid).exists():
			x=x+1
			rid=r+str(x)
		x=int(x)
		review_obj=UserReviews(Review_ID=rid,User_ID=userid,User_Name=user_name,Course_ID=Course_id,Review=review,Feedback=feedback)
		review_obj.save()
		return HttpResponse("<script>alert('ThankYou for your feedback..'); window.location.replace('/userdashboard/')</script>")
@csrf_exempt
def saveuser(request):
	if request.method=='POST':
		fname=request.POST.get('fname')
		lname=request.POST.get('lname')
		email=request.POST.get('email')
		mobile=request.POST.get('mobile')
		password=request.POST.get('password')
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
			dic={'checksession':check_user(request),
				'msg':'Incorrect OTP',
				'userid':uid}
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
	dic={'checksession':check_user(request),
		'msg':'OTP Sent',
		'userid':uid}
	return render(request,'verify.html',dic)
@csrf_exempt
def checklogin(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if UserData.objects.filter(User_Email=email,User_Password=password,Status='Active').exists():
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
		users=len(UserData.objects.all())
		courses=len(CourseData.objects.all())
		payment=0.0
		for x in PaymentData.objects.filter(RESPCODE='01'):
			payment=payment+float(x.TXNAMOUNT)
		dic={'users':users,'courses':courses,'payment':payment}
		#return redirect('/adminaddcourse/')
		return render(request,'adminpages/index.html',dic)
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminlogout(request):
	try:
		del request.session['adminid']
		request.session.flush()
		return redirect('/adminlogin/')
	except:
		return redirect('/index/')
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
	uid=request.session['userid']
	data=UserData.objects.filter(User_ID=uid).all()
	mycourse=UserCourses.objects.filter(UserID=uid,status=True)
	course_progress={}
	for i in mycourse:
		progress=get_Progress(request,i.Course_ID)
		course_progress[i.Course_ID]=progress
	#print(course_progress)

	course=CourseData.objects.all()
	return render(request,'userdashboard.html',{'data':data,'courses':course,'my_courses':mycourse,'course_progress':course_progress})
def courseplayer(request):
	uid=request.session['userid']
	course_id=request.GET.get('course_id')
	if UserCourses.objects.filter(UserID=uid,Course_ID=course_id,status=True).exists():
		lecture_data=LecturesData.objects.filter(Course_ID=course_id)
		course=CourseData.objects.filter(Course_ID=course_id)
		lecture_id=''
		for x in lecture_data:
			lecture_id=x.Lecture_ID
			break
		if UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id,Lecture_ID=lecture_id,
		Lecture_Watched=False).exists():
			
			userlec=UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id,Lecture_ID=lecture_id)
			for i in userlec:
				i.Lecture_Watched=True
				i.save()
		progress=get_Progress(request,course_id)
		#print(progress)
		Userlec=UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id).all()
		return render(request,'courseplayer.html',{'lecture_id':lecture_id,'course_data':course,'lecture_data':lecture_data,'userlec':Userlec,'progress':progress})
	else:
		return HttpResponse("<script>alert('Please enroll into the course'); window.location.replace('/userdashboard/')</script>")
def openlecture(request):
	lecture_id=request.GET.get('lecture')
	course_id=request.GET.get('course')
	lecture_data=LecturesData.objects.filter(Course_ID=course_id)
	course=CourseData.objects.filter(Course_ID=course_id)
	if UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id,Lecture_ID=lecture_id,
		Lecture_Watched=False).exists():
		userlec=UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id,Lecture_ID=lecture_id)
		for i in userlec:
			i.Lecture_Watched=True
			i.save()
	Userlec=UserLectures.objects.filter(User_ID=request.session['userid'],Course_ID=course_id).all()
	return render(request,'courseplayer.html',{'lecture_id':lecture_id,'course_data':course,'lecture_data':lecture_data,'userlec':Userlec})
def forget_password(request):
	if request.method=='POST':
		password=''
		email=request.POST['email']
		if UserData.objects.filter(User_Email=email).exists():

			data=UserData.objects.filter(User_Email=email)
			for x in data:
				password=x.User_Password
			sub='Edutern - Your Account Password'
			
			msg='''Hi there!
	Your Edutern Account Password is,

	'''+password+'''

	Thanks for creating your account on Edutern,
	Team Edutern'''
			email=EmailMessage(sub,data,to=[email])
			email.send()
			return HttpResponse("<script>alert('Your Password has been send to your mail'); window.location.replace('/login/')</script>")
	
		else:
			return HttpResponse("<script>alert('Email does not exists'); window.location.replace('/login/')</script>")
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
	try:
		adminid=request.session['adminid']
		data=UserData.objects.all()
		return render(request,'adminpages/userslist.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminactiveusers(request):
	try:
		adminid=request.session['adminid']
		data=UserData.objects.filter(Status='Active')
		return render(request,'adminpages/activeusers.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def makeuserdeactive(request):
	try:
		adminid=request.session['adminid']
		userid=request.GET.get('uid')
		UserData.objects.filter(User_ID=userid).update(Status='Deactive')
		return redirect('/adminactiveusers/')
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admindeactiveusers(request):
	try:
		adminid=request.session['adminid']
		data=UserData.objects.filter(Status='Deactive')
		return render(request,'adminpages/deactiveusers.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def makeuseractive(request):
	try:
		adminid=request.session['adminid']
		userid=request.GET.get('uid')
		UserData.objects.filter(User_ID=userid).update(Status='Active')
		return redirect('/admindeactiveusers/')
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admincourseenrolls(request):
	try:
		adminid=request.session['adminid']
		enrolls=UserCourses.objects.filter(status=True)
		return render(request,'adminpages/courseenrolls.html',{'data':enrolls})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admindeleteenrolls(request):
	try:
		adminid=request.session['adminid']
		cid=request.GET.get('cid')
		uid=request.GET.get('uid')
		pid=request.GET.get('pid')
		UserCourses.objects.filter(Pay_ID=pid).delete()
		UserLectures.objects.filter(UserID=uid,Course_ID=cid).delete()
		return redirect('/admincourseenrolls/')
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admincoursespayment(request):
	try:
		adminid=request.session['adminid']
		data=PaymentData.objects.all()
		return render(request,'adminpages/coursespayment.html',{'data':data})
	except:
		return redirect('/index/')
def adminuserreview(request):
	try:
		adminid=request.session['adminid']
		data=UserReviews.objects.all()
		return render(request,'adminpages/userreview.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def deletereview(request):
	try:
		adminid=request.session['adminid']
		rid=request.GET.get('rid')
		UserReviews.objects.filter(Review_ID=rid).delete()
		return redirect('/adminuserreview/')
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admincompletecourses(request):
	try:
		adminid=request.session['adminid']
		data=UserCourses.objects.all()
		dt,data_items=(),[]
		for i in data:
			dt=()
			total=UserLectures.objects.filter(User_ID=i.UserID_id,Course_ID=i.Course_ID).count()
			lecture_watched=UserLectures.objects.filter(User_ID=i.UserID_id,Course_ID=i.Course_ID,Lecture_Watched=True).count()
			if int(lecture_watched) == 0:
				progress=int(0)
				dt=(i.UserID_id,i.Course_ID,progress)
				data_items.append(dt)
			else:
				progress=int((lecture_watched/total)*100)
				dt=(i.UserID_id,i.Course_ID,progress)
				data_items.append(dt)
		return render(request,'adminpages/completecourses.html',{'data_items':data_items})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')	
def adminincompletecourses(request):
	try:
		adminid=request.session['adminid']
		data=UserCourses.objects.all()
		dt,data_items=(),[]
		for i in data:
			dt=()
			total=UserLectures.objects.filter(User_ID=i.UserID_id,Course_ID=i.Course_ID).count()
			lecture_watched=UserLectures.objects.filter(User_ID=i.UserID_id,Course_ID=i.Course_ID,Lecture_Watched=True).count()
			if lecture_watched == 0:
				progress=int(0)
				dt=(i.UserID_id,i.Course_ID,progress)
				data_items.append(dt)
			else:
				progress=int((lecture_watched/total)*100)
				dt=(i.UserID_id,i.Course_ID,progress)
				data_items.append(dt)
		return render(request,'adminpages/incompletecourses.html',{'data_items':data_items})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def reviewform(request):
	if request.method=='POST':
		userid=request.session['userid']
		user_fname=UserData.objects.filter(User_ID=userid).values('User_FName')[0]['User_FName']
		user_lname=UserData.objects.filter(User_ID=userid).values('User_LName')[0]['User_LName']
		review=request.POST['star']
		feedback=request.POST['feedback']
		Course_id=request.GET.get('course_id')
		user_name=user_fname+" "+user_lname
		review_obj=UserReviews(User_ID=userid,User_Name=user_name,Course_ID=Course_id,Review=review,Feedback=feedback)
		review_obj.save()
		return HttpResponse("<script>alert('ThankYou for your feedback..'); window.location.replace('/userdashboard/')</script>")
@csrf_exempt
def adminsendcertificate(request):
	if request.method=='POST':
		user=request.POST.get('user')
		course=request.POST.get('course')
		cert=request.FILES['cert']
		for x in UserData.objects.filter(User_ID=user):
			cid=uuid.uuid5(uuid.NAMESPACE_DNS, str(date.today().strftime("%d/%m/%Y"))+user+course)
			CertificatesData(Cert_ID=cid,Certificate=cert).save()
			msg='''Hi '''+x.User_FName+'''!
Cogratulations! on your course completion from Edutern.in,

You can download your certificate from the following link:

https://www.edutern.in/downloadcert/?certid='''+str(cid)+'''

Thanks & Regards,
Team Edutern'''
			sub='Edutern - Course Certificate'
			email=EmailMessage(sub,msg,to=[x.User_Email])
			email.send()
		return HttpResponse("<script>alert('Certificate Sent Successfully'); window.location.replace('/admincompletecourses/')</script>")
import requests
def downloadcert(request):
	certpath=''
	filename=''
	mid=request.GET.get('certid')
	if CertificatesData.objects.filter(Cert_ID=mid).exists():
		for x in CertificatesData.objects.filter(Cert_ID=mid):
			certpath=x.Certificate.url
			filename=x.Certificate
		url = certpath
		filename=str(filename)[5:len(str(filename))]
		r = requests.get(url, allow_redirects=True)
		filedownload = open(filename, 'wb').write(r.content)
		fl_path = filename
		file_path = filename
		file_wrapper = FileWrapper(open(filename, 'rb'))
		file_mimetype, _ = mimetypes.guess_type(file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype )
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Disposition'] = 'attachment; filename=%s' % file_path
		os.remove(filename)
		return response
	else:
		return HttpResponse("<script>alert('File Not Found'); window.location.replace('/index/')</script>")
def adminsendbulk(request):
	return render(request,'adminpages/sendbulk.html',{})
def adminsendtoone(request):
	return render(request,'adminpages/sendtoone.html',{})
def adminaddcoupons(request):
	if request.method=='POST':
		coupon_name=request.POST['coupon_name']
		coupon_code=request.POST['code']
		discount=int(request.POST['discount'])
		l="COU00"
		x=1
		lid=l+str(x)
		while CouponData.objects.filter(Coupon_ID=lid).exists():
			x=x+1
			lid=l+str(x)
		x=int(x)
		if CouponData.objects.filter(Coupon_Code=coupon_code).exists():
			return HttpResponse("Coupon Code already exists")
		else:
			data=CouponData(Coupon_ID=lid,Coupon_Name=coupon_name,Coupon_Code=coupon_code,Discount=discount)
			data.save()
			return redirect('/admincouponslist/')
	else:	
		return render(request,'adminpages/addcoupons.html',{})
def admincouponslist(request):
	try:
		adminid=request.session['adminid']
		data=CouponData.objects.all()
		return render(request,'adminpages/couponslist.html',{'data':data})
	except:
		return redirect('/index/')
def admindeletecoupon(request):
	try:
		adminid=request.session['adminid']
		coupon_id=request.GET.get('cid')
		data=CouponData.objects.filter(Coupon_ID=coupon_id).delete()
		return redirect('/admincouponslist/')
	except:
		return redirect('/index/')

def instructorform(request):
	if request.method=='POST':
		name=request.POST['fname']
		mobile=request.POST['mobile']
		email=request.POST['email']
		sub='Edutern - 	A NEW INSTRUCTOR FILL THE FORM'
		msg='Name : {}\n Email : {} \n Mobile :{}'.format(name,email,mobile)
		#print(msg)
		email=EmailMessage(sub,msg,to=['shreshtharnd20@gmail.com'])
		email.send()
		return HttpResponse("<script>alert('Your query has been submitted succesfully'); window.location.replace(/index/)</script>")
def enquiryform(request):
	if request.method=='POST':
		name=request.POST['fname']
		mobile=request.POST['mobile']
		email=request.POST['email']
		sub='Edutern - 	A NEW USER FILL THE ENQUIRY FORM'
		msg='Name : {}\n Email : {} \n Mobile :{}'.format(name,email,mobile)
		#print(msg)
		email=EmailMessage(sub,msg,to=['shreshtharnd20@gmail.com'])
		email.send()
		return HttpResponse("<script>alert('Your query has been submitted succesfully'); window.location.replace(/index/)</script>")

#Payment Code
import app.Checksum as Checksum
def checkout(request):
	if request.method=='GET':
		course_id=request.GET.get('course_id')
		user_id=request.session['userid']
		l="PAY00"
		x=1
		lid=l+str(x)
		while UserCourses.objects.filter(Pay_ID=lid).exists():
			x=x+1
			lid=l+str(x)
		x=int(x)
		usercourse=UserCourses(Pay_ID=lid,UserID_id=user_id,Course_ID=course_id,status=False)
		usercourse.save()
		'''lectures=LecturesData.objects.filter(Course_ID=course_id).all()
		if UserCourses.objects.filter(UserID_id=user_id,Course_ID=course_id,status=True).exists():
			for i in lectures:
				dt=UserLectures(User_ID=user_id,Course_ID=i.Course_ID,Lecture_ID=i.Lecture_ID,Lecture_Watched=False)
				dt.save()'''
		amount=''
		for x in CourseData.objects.filter(Course_ID=course_id):
			amount=x.Course_Fee
		dic={
			'ORDER_ID':lid,
			'TXN_AMOUNT':str(amount),
			'CUST_ID':user_id,
			'INDUSTRY_TYPE_ID':'Retail',
			'CHANNEL_ID':'WEB',
			'WEBSITE':'WEBSTAGING',
			'CALLBACK_URL':'http://127.0.0.1:8000/verifypayment/'
		}
		MERCHANT_KEY = 'gDokYWVAFFW9OSlZ'
		MID = 'bAQrse69179758299775'
		data_dict = {'MID':MID}
		data_dict.update(dic)
		param_dict = data_dict
		param_dict['CHECKSUMHASH'] =Checksum.generateSignature(data_dict, MERCHANT_KEY)
		param_dict.update({'coupon':CouponData.objects.all(),'checksession':check_user(request),'course_data':CourseData.objects.filter(Course_ID=course_id)})
		return render(request,'checkout.html',param_dict)
	else:
		return redirect('/index/')
@csrf_exempt
def applypromocode(request):
	course_id=request.GET.get('courseid')
	promo=request.GET.get('promo')
	user_id=request.session['userid']
	l="PAY00"
	x=1
	lid=l+str(x)
	while UserCourses.objects.filter(Pay_ID=lid).exists():
		x=x+1
		lid=l+str(x)
	x=int(x)
	usercourse=UserCourses(Coupon=promo,Pay_ID=lid,UserID_id=user_id,Course_ID=course_id,status=False)
	usercourse.save()
	amount=0
	discount=0
	for x in CouponData.objects.filter(Coupon_ID=promo):
		discount=int(x.Discount)
	for x in CourseData.objects.filter(Course_ID=course_id):
		amount=int(x.Course_Fee)
	amounttopay=amount-((amount/100)*discount)
	dic={
		'ORDER_ID':lid,
		'TXN_AMOUNT':str(amounttopay),
		'CUST_ID':user_id,
		'INDUSTRY_TYPE_ID':'Retail',
		'CHANNEL_ID':'WEB',
		'WEBSITE':'WEBSTAGING',
		'CALLBACK_URL':'http://127.0.0.1:8000/verifypayment/'
	}
	MERCHANT_KEY = 'gDokYWVAFFW9OSlZ'
	MID = 'bAQrse69179758299775'
	data_dict = {'MID':MID}
	data_dict.update(dic)
	param_dict = data_dict
	param_dict['CHECKSUMHASH'] =Checksum.generateSignature(data_dict, MERCHANT_KEY)
	param_dict.update({'coupon':CouponData.objects.all(),'checksession':check_user(request),'course_data':CourseData.objects.filter(Course_ID=course_id)})
	return render(request,'checkout.html',param_dict)
import cgi
@csrf_exempt
def verifypayment(request):
		MERCHANT_KEY = 'gDokYWVAFFW9OSlZ'
		MID = 'bAQrse69179758299775'
		CURRENCY=request.POST.get('CURRENCY')
		GATEWAYNAME=request.POST.get('GATEWAYNAME')
		RESPMSG=request.POST.get('RESPMSG')
		BANKNAME=request.POST.get('BANKNAME')
		PAYMENTMODE=request.POST.get('PAYMENTMODE')
		RESPCODE=request.POST.get('RESPCODE')
		TXNID=request.POST.get('TXNID')
		TXNAMOUNT=request.POST.get('TXNAMOUNT')
		ORDERID=request.POST.get('ORDERID')
		STATUS=request.POST.get('STATUS')
		BANKTXNID=request.POST.get('BANKTXNID')
		TXNDATE=request.POST.get('TXNDATE')
		CHECKSUMHASH=request.POST.get('CHECKSUMHASH')
		respons_dict = {
						'MERCHANT_KEY':MERCHANT_KEY,
						'CURRENCY':CURRENCY,
						'GATEWAYNAME':GATEWAYNAME,
						'RESPMSG':RESPMSG,
						'BANKNAME':BANKNAME,
						'PAYMENTMODE':PAYMENTMODE,
						'MID':MID,
						'RESPCODE':RESPCODE,
						'TXNID':TXNID,
						'TXNAMOUNT':TXNAMOUNT,
						'ORDERID':ORDERID,
						'STATUS':STATUS,
						'BANKTXNID':BANKTXNID,
						'TXNDATE':TXNDATE,
						'CHECKSUMHASH':CHECKSUMHASH
		}
		checksum=respons_dict['CHECKSUMHASH']
		if 'GATEWAYNAME' in respons_dict:
			if respons_dict['GATEWAYNAME'] == 'WALLET':
				respons_dict['BANKNAME'] = 'null';
		obj=PaymentData(
			Pay_ID=ORDERID,
			CURRENCY=CURRENCY,
			GATEWAYNAME=str(GATEWAYNAME),
			RESPMSG=RESPMSG,
			BANKNAME=str(BANKNAME),
			PAYMENTMODE=str(PAYMENTMODE),
			RESPCODE=RESPCODE,
			TXNID=str(TXNID),
			TXNAMOUNT=TXNAMOUNT,
			STATUS=STATUS,
			BANKTXNID=BANKTXNID,
			TXNDATE=str(TXNDATE),
			CHECKSUMHASH=str(CHECKSUMHASH)
			)
		obj.save()
		obj=UserCourses.objects.filter(Pay_ID=ORDERID)
		for x in obj:
			request.session['userid']=str(x.UserID)
		custid=request.session['userid']
		data_dict = {
			'MID':respons_dict['MID'],
			'ORDER_ID':ORDERID,
			'TXN_AMOUNT':TXNAMOUNT,
			'CUST_ID':custid,
			'INDUSTRY_TYPE_ID':'Retail',
			'CHANNEL_ID':'WEB',
			'WEBSITE':'WEBSTAGING',
			'CALLBACK_URL':'http://127.0.0.1:8000/verifypayment/'
			}
		checksum =Checksum.generateSignature(data_dict, MERCHANT_KEY)
		print('Hello')
		verify = Checksum.verifySignature(data_dict, MERCHANT_KEY, checksum)
		if verify:
			if respons_dict['RESPCODE'] == '01':
				obj=UserCourses.objects.filter(Pay_ID=ORDERID)
				obj.update(status=True)
				dic={'TXNID':TXNID}
				for x in obj:
					lectures=LecturesData.objects.filter(Course_ID=x.Course_ID).all()
					if UserCourses.objects.filter(Pay_ID=ORDERID,UserID_id=request.session['userid'],Course_ID=x.Course_ID,status=True).exists():
						for i in lectures:
							dt=UserLectures(User_ID=user_id,Course_ID=i.Course_ID,Lecture_ID=i.Lecture_ID,Lecture_Watched=False)
							dt.save()
					for y in CourseData.objects.filter(Course_ID=x.Course_ID):
						dic.update({'COURSE':y.Course_Name,
									'checksession':check_user(request)})
				return render(request,'paysuccess.html',dic)
			else:
				dic={'TXNID':TXNID,
					'RESPMSG':RESPMSG,
					'checksession':check_user(request)}
				return render(request,'payfailed.html',dic)
		else:
			dic={'TXNID':TXNID,
					'RESPMSG':RESPMSG,
					'checksession':check_user(request)}
			return render(request,'payfailed.html',dic)

def downloaddatabase(request):
	try:
		aid=request.session['adminid']
		table=request.GET.get('tablename')
		return downloaddata(table)
	except:
		return redirect('/index/')