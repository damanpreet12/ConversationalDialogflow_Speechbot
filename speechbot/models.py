from django.db import models

# Create your models here.
class UserDetails(models.Model):
    userid=models.AutoField(primary_key=True)

    firstname=models.CharField(max_length=200,default="")
    lastname=models.CharField(max_length=200,default="")
    age=models.IntegerField(default="")
    gender = models.CharField(max_length=400, default="")
    email = models.CharField(max_length=200, default="")
    address=models.CharField(max_length=400,default="")
    statecode=models.CharField(max_length=200,default="")