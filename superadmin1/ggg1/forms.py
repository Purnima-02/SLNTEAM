from django import forms
from django.core.exceptions import ValidationError
from .models import HRCredentials
import re

class HRCredentialsForm(forms.ModelForm):
    class Meta:
        model = HRCredentials
        fields = [
            'employee_id', 'hr_name', 'email', 'phone_number', 
            'aadhar_number', 
            'pan_number', 'password', 'is_active'
        ]
        widgets = {
            'password': forms.PasswordInput(),  # Hide password input
        }

    def clean_aadhar_number(self):
        aadhar = self.cleaned_data.get('aadhar_number')
        if not re.match(r'^\d{12}$', aadhar):  # Aadhar should be exactly 12 digits
            raise ValidationError("Aadhar number must be a 12-digit number.")
        return aadhar

    def clean_pan_number(self):
        pan = self.cleaned_data.get('pan_number')
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):  # PAN format check
            raise ValidationError("PAN number must be in the format: 5 letters, 4 digits, 1 letter.")
        return pan

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Enforce a strong password policy
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', password):
            raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        return password
