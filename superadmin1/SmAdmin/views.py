from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings

      

import logging

logger = logging.getLogger(__name__)

def hrEduViewsets(request):
     return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}el/loan-records/"})

def hrgoldapi(request):
      return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}goldview/"})


from django.conf import settings
def hrplapi(request):
  return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}pl/personallist/"})

def hrlapapi(request):
     return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}lapview/"})

def hrhlapi(request):
      return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}pl/homelist/"})

def hrBusiViewsets(request):
     return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}bl/business-loans-lists"})


def hrddproject(request):
     return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}cl/car-loans-list/"})

def hrapi_credit_appli(request):
   return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}cc/table_view/"})

def hrotherapi(request):
    return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}otherview/"})


def hrviewinsurance(request):
    return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewinsurance/"})

def hrviewlifeinsurance(request):
    return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewlifeinsurance/"})

def hrviewhealthinsurance(request):
    return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewhealthinsurance/"})
def hrviewgeninsurance(request):
    return render(request,"register/superad.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewgeninsurance/"})




import requests
from SmAdmin.models import *

#anushahttp://127.0.0.1:999/branch/agreerecords/
import requests
from django.shortcuts import render
from django.conf import settings
from .models import franchise  # Make sure to import your franchise model
from django.http import JsonResponse

def hrfranchise_view(request):
    url = f"{settings.HR_SOURCE_URL}/manager/branch/agreerecords/"
    
    try:
        # Make the request with SSL verification turned off
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Will raise an error if the response code is not 200

        # Check if the response content type is JSON before parsing
        if response.headers.get('Content-Type') == 'application/json':
            data = response.json()  # Attempt to parse JSON
        else:
            return JsonResponse({'error': 'Unexpected response format (not JSON)'}, status=500)

    except requests.exceptions.RequestException as e:
        # Handle network or server errors
        return JsonResponse({'error': f'Request failed: {str(e)}'}, status=500)

    except ValueError:
        # Handle JSON decoding errors
        return JsonResponse({'error': 'Response content is not valid JSON'}, status=500)

    # Process the JSON data if available
    for item in data:
        franchise_id = item.get('franchise_id')
        email = item.get('email')
        phone = item.get('phone')
        name = item.get('name')
        pan = item.get('pan')
        aadhar = item.get('aadhar')
        profession = item.get('profession')
        city = item.get('city')
        agreeCheck = item.get('agreeCheck')
        dsaPhoto = item.get('dsaPhoto')
        aadharFront = item.get('aadharFront')
        aadharBack = item.get('aadharBack')
        panCard = item.get('panCard')
        bankDocument = item.get('bankDocument')

        # Use update_or_create to either update an existing record or create a new one
        franchis, created = franchise.objects.update_or_create(
            franchise_id=franchise_id,  # Use franchise_id as the unique identifier
            defaults={
                'name': name,
                'email': email,
                'phone': phone,
                'pan': pan,
                'aadhar': aadhar,
                'profession': profession,
                'city': city,
                'agreeCheck': agreeCheck,
                'dsaPhoto': dsaPhoto,
                'aadharFront': aadharFront,
                'aadharBack': aadharBack,
                'panCard': panCard,
                'bankDocument': bankDocument
            }
        )
    
    # Fetch all franchises to display on the HTML page
    branch = franchise.objects.all()
    return render(request, 'register/hrfranchise.html', {'branch': branch})

            
        #     # Assuming dsaPhoto, aadharFront, aadharBack, panCard, and bankDocument are in base64 format
from django.http import HttpResponse           
def approve_employee(request, employee_id):
    # Approve the franchise
    employee = get_object_or_404(franchise, id=employee_id)
    employee.aproval_status = 'approved'
    employee.save()
    return HttpResponse('<h1>Approved Succesfully</h1>')

def approved_franchises(request):
    # Fetch only approved franchises
    approved_franchises = franchise.objects.filter(aproval_status='approved')
    return render(request, 'register/franchiseapprove.html', {'approved_franchises': approved_franchises})  

def reject_employee(request, employee_id):
    # Fetch only rejected franchises
    employee = get_object_or_404(franchise, id=employee_id)
    employee.aproval_status = 'rejected'
    employee.save()
    return HttpResponse('<h1>Rejected</h1>')

def rejected_franchises(request):
    # Reject the franchise
    approved_franchises = franchise.objects.filter(aproval_status='rejected')
    return render(request, 'register/reject.html', {'approved_franchises': approved_franchises})
