from django.db import models
from django.conf import settings
from datetime import date

class CourseData(models.Model):
	Course_ID=models.CharField(max_length=20, primary_key=True)
	Course_Name=models.CharField(max_length=100)
	Course_Trainer=models.CharField(max_length=100)
	Course_Fee=models.CharField(max_length=50)
	Course_Objective=models.CharField(max_length=1000)
	Course_Eligibility=models.CharField(max_length=1000)
	Course_Thumb=models.FileField(upload_to='coursethumb/')
	class Meta:
		db_table="CourseData"


class LecturesData(models.Model):
	Lecture_ID=models.CharField(max_length=20, primary_key=True)
	Course_ID=models.CharField(max_length=20)
	Lecture_Name=models.CharField(max_length=100)
	Lecture_Video=models.FileField(upload_to='courselectures/')
	class Meta:
		db_table="LecturesData"

class UserData(models.Model):
	Join_Date=models.CharField(max_length=50, default=date.today().strftime("%d/%m/%Y"))
	User_ID=models.CharField(max_length=20, primary_key=True)
	User_FName=models.CharField(max_length=50, default='NA')
	User_LName=models.CharField(max_length=50, default='NA')
	User_Email=models.CharField(max_length=70, default='NA')
	User_Phone=models.CharField(max_length=15, default='NA')
	User_Password=models.CharField(max_length=20, default='NA')
	Verify_Status=models.CharField(max_length=12, default='Unverified')
	Status=models.CharField(max_length=10, default='Active')
	class Meta:
		db_table="UserData"
	def __str__(self):
		return str(self.User_ID)

class UserCourses(models.Model):
	UserID=models.ForeignKey(UserData,on_delete=models.CASCADE,null=True,blank=True)
	Course_ID=models.CharField(max_length=20)
	status=models.BooleanField(default=False)
class UserReviews(models.Model):
	Review_ID=models.CharField(max_length=20,primary_key=True)
	User_ID=models.CharField(max_length=20,null=True,blank=True)
	User_Name=models.CharField(max_length=200,null=True,blank=True)
	Course_ID=models.CharField(max_length=20,null=True,blank=True)
	Review=models.CharField(max_length=5,null=True,blank=True)
	Feedback=models.TextField(max_length=200,blank=True,null=True)
	def __str__(self):
		return self.Review
class UserLectures(models.Model):
	User_ID=models.CharField(max_length=20,null=True,blank=True)
	Course_ID=models.CharField(max_length=20,null=True,blank=True)
	Lecture_ID=models.CharField(max_length=20,null=True,blank=True)
	Lecture_Watched=models.BooleanField(default=False)

class CertificatesData(models.Model):
	Cert_ID=models.CharField(max_length=20, primary_key=True)
	Certificate=models.FileField(upload_to='cert/')
	class Meta:
		db_table="CertificatesData"

class CouponData(models.Model):
	Coupon_ID=models.CharField(max_length=20,primary_key=True)
	Coupon_Name=models.CharField(max_length=200)
	Coupon_Code=models.CharField(max_length=200)
	Discount=models.IntegerField()
	def __str__(self):
		return self.Coupon_ID
