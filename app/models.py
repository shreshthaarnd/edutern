from django.db import models
from django.conf import settings

class CourseData(models.Model):
	Course_ID=models.CharField(max_length=20, primary_key=True)
	Course_Name=models.CharField(max_length=100)
	Course_Trainer=models.CharField(max_length=100)
	Course_Fee=models.CharField(max_length=50)
	Course_Objective=models.CharField(max_length=1000)
	Course_Eligibility=models.CharField(max_length=1000)
	Course_Content=models.CharField(max_length=1000)
	Course_Thumb=models.FileField(upload_to='coursethumb/')
	class Meta:
		db_table="CourseData"