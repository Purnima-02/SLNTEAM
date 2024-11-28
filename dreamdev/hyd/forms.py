from django import forms
from django.core.exceptions import ValidationError
from .models import Ticket, DSATicket, FranchiseeTicket
import re

# Custom validators
def validate_name(value):
    if not re.match("^[a-zA-Z\s]*$", value):
        raise ValidationError("Name must contain only letters and spaces.")

def validate_phone_number(value):
    if not re.match("^\d{10}$", str(value)):
        raise ValidationError("Phone number must be exactly 10 digits.")

def validate_related_application_number(value):
    if not re.match("^\d+$", str(value)):
        raise ValidationError("Related application number must contain only numbers.")
    
def validate_email(value):
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        raise ValidationError("Invalid email address format.")

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'phone_number', 'email', 'issue_type', 'description', 'related_application_number', 'supporting_documents',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'issue_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class':  'form-control'}),
            'related_application_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'supporting_documents': forms.FileInput(attrs={'class': 'form-control'})
        }

    # Custom validation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_name(name)
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate_phone_number(phone_number)
        return phone_number


class DSATicketForm(forms.ModelForm):
    class Meta:
        model = DSATicket
        fields = ['issue_type', 'name', 'phone_number', 'email','description']
        widgets = {
            'issue_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class':  'form-control'})
        }

    # Custom validation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_name(name)
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate_phone_number(phone_number)
        return phone_number


class FranchiseeTicketForm(forms.ModelForm):
    class Meta:
        model = FranchiseeTicket
        fields = ['issue_type', 'name', 'phone_number', 'description','email',]
        widgets = {
            'issue_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class':  'form-control'})
        }

    # Custom validation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_name(name)
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate_phone_number(phone_number)
        return phone_number

