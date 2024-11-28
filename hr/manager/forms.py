# forms.py

from django import forms
from .models import *

class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['username','password','phone_number','email','employee_type','franchisecode',]
        exculde = ['employee_id']

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.set_password(self.cleaned_data["password"])
        if commit:
            employee.save()
        return employee


class EmployeeLoginForm(forms.Form):
    employee_id = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)



class SalesRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Sales
        fields = ['registerid', 'password', 'franchiseCode']

class DSAUsersRegistrationForm(forms.ModelForm):
    dsa_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = DSAUsers
        fields = ['dsa_registerid', 'dsa_name', 'dsa_password', 'franchiseCode']

class FranchiseUsersRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = FranchiseUsers
        fields = ['franchise_id', 'name', 'password']

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = custmer
        fields = ['franchise_id', 'name', 'password']

class franchisesalesForm(forms.ModelForm):
    class Meta:
        model=franchisesales
        fields='__all__'