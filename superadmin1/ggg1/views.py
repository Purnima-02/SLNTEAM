from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import HRCredentialsForm
from .models import HRCredentials


# def hr_credentials_view(request):
#     if request.method == 'POST':
#         form = HRCredentialsForm(request.POST)
#         if form.is_valid():
#             hr_credential = form.save(commit=False)
#             hr_credential.password = form.cleaned_data['password']  # Hash password if necessary
#             hr_credential.save()
#             return redirect('success')  # Redirect to a success page
#     else:
#         form = HRCredentialsForm()
#     return render(request, 'hr_credentials_form.html', {'form': form})


def hr_credentials_view(request):
    success = False  
    if request.method == 'POST':
        form = HRCredentialsForm(request.POST)
        if form.is_valid():
            hr_credential = form.save(commit=False)
            hr_credential.password = form.cleaned_data['password']  
            hr_credential.save()
            success = True  
            form = HRCredentialsForm() 
    else:
        form = HRCredentialsForm()
    return render(request, 'hr_credentials_form.html', {'form': form, 'success': success})





from django.shortcuts import render, redirect, get_object_or_404
from .forms import HRCredentialsForm
from .models import HRCredentials

from django.shortcuts import render, redirect, get_object_or_404
from .forms import HRCredentialsForm
from .models import HRCredentials


def hr_credentials_views(request):
    hr_credentials = HRCredentials.objects.filter(is_active=True)

    if request.method == 'POST':
        if 'deactivate' in request.POST:
            credential_id = request.POST['deactivate']
            credential = get_object_or_404(HRCredentials, id=credential_id)
            credential.is_active = False
            credential.save()
            return redirect('hrform')  # Redirect to the same view

    return render(request, 'hr_credentials_table.html', {'hr_credentials': hr_credentials})




















# Create your views here.
def customersupport(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/open_tickets/"})
def customersupport1(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/inprogress_tickets/"})   

def customersupport2(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/resolved_tickets/"})


def customersupport3(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/DSA_open_tickets_view/"})
def customersupport4(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/DSA_inprogress_tickets/"})   

def customersupport5(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/DSA_resolved_tickets/"})


def customersupport6(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/Franchisee_open_tickets_view/"})
def customersupport7(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/Franchisee_inprogress_tickets/"})   

def customersupport8(request):
  return render(request,"customer.html",{'url':f"{settings.CUSTOMER_SUPPORT_URL}/Franchisee_resolved_tickets/"})