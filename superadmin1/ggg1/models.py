from django.db import models



class HRCredentials(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)  # Unique identifier
    hr_name = models.CharField(max_length=100)  # HR name
    email = models.EmailField(unique=True)       # Email for login
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone field
    aadhar_number = models.CharField(max_length=12, unique=True)  # Aadhar number
    pan_number = models.CharField(max_length=10, unique=True)     # PAN number
    password = models.CharField(max_length=50)  # Password field
    is_active = models.BooleanField(default=True) # Status to verify active users

    def __str__(self):
        return f"{self.hr_name} ({self.employee_id})"
