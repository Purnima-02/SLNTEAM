# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser 



class Employee(AbstractUser):
    EMPLOYEE_TYPE_CHOICES = [
        ('Backendemployee', 'Loan Process Backend'),
        ('Accounts','Accounts'),
        ('customersupport','Customer Support'),
        ('sales','sales')
        ]
    
    employee_id = models.CharField(max_length=10, unique=True)
    employee_type = models.CharField(choices=EMPLOYEE_TYPE_CHOICES, max_length=20)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    franchisecode =models.CharField(max_length=100)
    


    def __str__(self):
        return self.username



class dsa(models.Model):
    # dsa_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    # name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10)
    pan = models.CharField(max_length=12, null=True, blank=True)
    aadhar = models.CharField(max_length=12)
    profession = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    acc_number = models.CharField(max_length=30)
    acc_holder_name = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=40)
    branch_name = models.CharField(max_length=20)
    agreeCheck = models.BooleanField(default=False)
    dsa_registerid=models.CharField(max_length=100 ,null=True,blank=True)
    dsa_name=models.CharField(max_length=100,null=True,blank=True)
    franchiseCode=models.CharField(max_length=100,null=True)
    # New field to track approval status
    approval_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='pending')

    def __str__(self):
        return self.name    
    
from django.core.exceptions import ValidationError


def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    extension = value.name.split('.')[-1].lower()
    if f".{extension}" not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, and PNG files are allowed.')


    
class franchise(models.Model):
    franchise_id=models.CharField(max_length=1000,unique=True,null=True,blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=15,null=True)  # Allow null and blank values
    pan=models.CharField(max_length=12,null=True,blank=True)
    aadhar=models.CharField(max_length=12)
    profession=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    agreeCheck=models.BooleanField(default=False)
    dsaPhoto=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    aadharFront=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    aadharBack=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    panCard=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    bankDocument=models.ImageField(validators=[validate_image_file],upload_to='dsa/')
    # New field to track approval status
    aproval_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='pending')



    def __str__(self):
       return self.name

class franchisesales(models.Model):
    Employe = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    registerid=models.CharField(max_length=100,null=True)
    franchiseCode=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10,null=True)
    pan = models.CharField(max_length=12, null=True, blank=True) #No Update...
    aadhar = models.CharField(max_length=12,null=True) #No Update.....
    qualification = models.CharField(max_length=30,null=True)
    approval_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='pending')
 

class Sales(models.Model):
    registerid=models.CharField(max_length=100,default='')
    password=models.CharField(max_length=200,null=True,blank=True)
    franchiseCode=models.CharField(max_length=100,null=True)

class DSAUsers(models.Model):
    dsa_registerid=models.CharField(max_length=100,null=True)
    dsa_name=models.CharField(max_length=100,null=True)
    dsa_password=models.CharField(max_length=200,null=True,blank=True)
    franchiseCode=models.CharField(max_length=100,null=True)
   

class FranchiseUsers(models.Model):
    franchise_id=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=100,null=True)
   
class custmer(models.Model):
    franchise_id = models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class HRcredentials(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
