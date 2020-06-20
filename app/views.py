from django.shortcuts import render

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
def adminindex(request):
	return render(request,'adminpages/index.html',{})
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def admincodorderlist(request):
	return render(request,'adminpages/codorderlist.html',{})
def login(request):
	return render(request,'login.html',{})
def registration(request):
	return render(request,'registration.html',{})