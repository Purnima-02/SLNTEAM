from django.db import models
from django.core.exceptions import ValidationError

def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    extension = value.name.split('.')[-1].lower()
    if f".{extension}" not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, and PNG files are allowed.')
# Create your models here.
class franchise(models.Model):
    franchise_id=models.CharField(max_length=255,unique=True,null=True,blank=True,db_index=True)
    name=models.CharField(max_length=20,db_index=True)
    email=models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,db_index=True)  # Allow null and blank values
    pan=models.CharField(max_length=12,null=True,blank=True,db_index=True)
    aadhar=models.CharField(max_length=12,db_index=True)
    profession=models.CharField(max_length=30,db_index=True)
    city=models.CharField(max_length=30,db_index=True)
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
