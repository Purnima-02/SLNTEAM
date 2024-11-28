from django.shortcuts import render,redirect,get_object_or_404
import requests
from django.http import HttpResponse
from .models import *
from .forms import *
from django.core.paginator import Paginator
from datetime import datetime
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def fetch_and_store_data(request):
    url = f"{settings.SOURCE_PROJECT_URL}getdisbursementdetails"
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        return HttpResponse("Failed to fetch data from API")

    try:
        data = response.json()
        print(data)  # Check the entire response structure

        # Function to process items
        def process_item(item):
            application_id = item.get('application_id')
            fran_code = item.get('franrefCode')
            dsa_code = item.get('dsaref_code')
            created_at=item.get('created_at')
            # Skip items with missing application_id
            if not application_id:
                print("Skipping item with missing application_id:", item)
                return
            
            # Directly use 'name' if it exists at the top level
            name = item.get('name')

            # Only attempt to construct 'name' if it is not available
            if not name:
                basic_detail = item.get('basicdetailform') or item.get('basicdetailhome')
                if basic_detail:
                    fname = basic_detail.get('fname', '')
                    lname = basic_detail.get('lname', '')
                    name = f"{fname} {lname}".strip() if fname or lname else None

            # Print an error if the name is still None
            if name is None:
                print("Missing 'name' for item:", item)
                return

            # Accessing disbursement detail
            verification_info = item.get('disbursementdetail', {})
            if not isinstance(verification_info, dict):
                print("Disbursement detail is not a dictionary:", verification_info)
                return

            # Extracting required fields
            disbursement_data = {
                'bank_nbfc_name': verification_info.get('bank_nbfc_name'),
                'disbursement_date': verification_info.get('disbursement_date'),
                'net_disbursement': verification_info.get('net_disbursement'),
                'mobile_no': verification_info.get('mobile_no'),
                'loan_amount': verification_info.get('loan_amount'),
                'location': verification_info.get('location'),
                'bank_loginid': verification_info.get('bank_loginid'),
                'bank_person_name': verification_info.get('bank_person_name'),
                'tenure': verification_info.get('tenure'),
                'roi': verification_info.get('roi'),
                'insurance': verification_info.get('insurance'),

            }

            # Store DisbursementData
            disbursement, created = DisbursementData.objects.get_or_create(
                application_id=application_id,
                name=name,
                defaults={'fran_code': fran_code, 'dsa_code': dsa_code,'created_at':created_at}
            )

            if created:
                print(f"Stored Disbursement: {application_id}")
            else:
                print(f"Disbursement already exists for: {application_id}")

            # Store DisbursementDetail
            if not DisbursementDetail.objects.filter(disbursement=disbursement).exists():
                DisbursementDetail.objects.create(disbursement=disbursement, **disbursement_data)
                print(f"Stored DisbursementDetail for: {application_id}")
            else:
                print(f"DisbursementDetail already exists for application_id: {application_id}")

        # Process each type of data item
        for item in data.get('personal_details', []):
            print("Processing personal_detail:", item)
            process_item(item)

        for item in data.get('loan_applications', []):
            print("Processing loan_application:", item)
            process_item(item)
        
        for item in data.get('home_applications', []):
            print("Processing home_application:", item)
            process_item(item)

        for item in data.get('car_applications', []):
            print("Processing car_application:", item)
            process_item(item)

        for item in data.get('bus_applications', []):
            print("Processing bus_application:", item)
            process_item(item)

        for item in data.get('edu_applications', []):
            print("Processing edu_application:", item)
            process_item(item)

        return HttpResponse("Data fetched and stored successfully")

    except ValueError as e:
        print("Error parsing JSON:", e)
        return HttpResponse("Error parsing response JSON")

from django.core.paginator import Paginator

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests

def disbursement_list(request):
    url = f"{settings.SOURCE_PROJECT_URL}getdisbursementdetails"
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        return HttpResponse("Failed to fetch data from API")

    try:
        data = response.json()
        print(data)  # Check the entire response structure

        # Function to process items
        def process_item(item):
            application_id = item.get('application_id')
            fran_code = item.get('franrefCode')
            dsa_code = item.get('dsaref_code')
            created_at = item.get('created_at')
            
            # Skip items with missing application_id
            if not application_id:
                print("Skipping item with missing application_id:", item)
                return
            
            # Directly use 'name' if it exists at the top level
            name = item.get('name')
            
            # Only attempt to construct 'name' if it is not available
            if not name:
                basic_detail = item.get('basicdetailform') or item.get('basicdetailhome')
                if basic_detail:
                    fname = basic_detail.get('fname', '')
                    lname = basic_detail.get('lname', '')
                    name = f"{fname} {lname}".strip() if fname or lname else None

            # Print an error if the name is still None
            if name is None:
                print("Missing 'name' for item:", item)
                return

            # Accessing disbursement detail
            verification_info = item.get('disbursementdetail', {})
            if not isinstance(verification_info, dict):
                print("Disbursement detail is not a dictionary:", verification_info)
                return

            # Extracting required fields
            disbursement_data = {
                'bank_nbfc_name': verification_info.get('bank_nbfc_name'),
                'disbursement_date': verification_info.get('disbursement_date'),
                'net_disbursement': verification_info.get('net_disbursement'),
                'mobile_no': verification_info.get('mobile_no'),
                'loan_amount': verification_info.get('loan_amount'),
                'location': verification_info.get('location'),
                'bank_loginid': verification_info.get('bank_loginid'),
                'bank_person_name': verification_info.get('bank_person_name'),
                'tenure': verification_info.get('tenure'),
                'roi': verification_info.get('roi'),
                'insurance': verification_info.get('insurance'),
            }

            # Store DisbursementData
            disbursement, created = DisbursementData.objects.get_or_create(
                application_id=application_id,
                name=name,
                defaults={'fran_code': fran_code, 'dsa_code': dsa_code, 'created_at': created_at}
            )

            if created:
                print(f"Stored Disbursement: {application_id}")
            else:
                print(f"Disbursement already exists for: {application_id}")

            # Store DisbursementDetail
            if not DisbursementDetail.objects.filter(disbursement=disbursement).exists():
                DisbursementDetail.objects.create(disbursement=disbursement, **disbursement_data)
                print(f"Stored DisbursementDetail for: {application_id}")
            else:
                print(f"DisbursementDetail already exists for application_id: {application_id}")

        # Process each type of data item
        for item in data.get('personal_details', []):
            print("Processing personal_detail:", item)
            process_item(item)

        for item in data.get('loan_applications', []):
            print("Processing loan_application:", item)
            process_item(item)
        
        for item in data.get('home_applications', []):
            print("Processing home_application:", item)
            process_item(item)

        for item in data.get('car_applications', []):
            print("Processing car_application:", item)
            process_item(item)

        for item in data.get('bus_applications', []):
            print("Processing bus_application:", item)
            process_item(item)

        for item in data.get('edu_applications', []):
            print("Processing edu_application:", item)
            process_item(item)

    except ValueError as e:
        print("Error processing data:", e)
        return HttpResponse("Error processing data from API")

    # Handle search and filter options
    search_query = request.GET.get('search', '').strip()
    disbursements = DisbursementDetail.objects.all()

    if search_query:
        disbursements = disbursements.filter(disbursement__application_id__icontains=search_query)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            disbursements = disbursements.filter(disbursement_date__range=[start_date, end_date])
        except ValueError:
            pass

    paginator = Paginator(disbursements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Input window processing
    for detail in page_obj:
        if detail.disbursement:
            detail.disbursement_id = detail.disbursement.id
            detail.input_window_exists = InputWindow.objects.filter(disbursement=detail.disbursement).exists()
            detail.output_window_exists = Disbursement.objects.filter(disbursement=detail.disbursement).exists()
            detail.settle_window_exists = SettlementWindow.objects.filter(disbursement=detail.disbursement).exists()
            detail.refid = detail.disbursement.refid if detail.disbursement.refid else 'N/A'
            detail.franchrefid = detail.disbursement.franchrefid if detail.disbursement.refid else 'N/A'
            print(f"Application ID: {detail.disbursement.application_id}, Ref ID: {detail.refid}, Franch Ref ID: {detail.franchrefid}")

    # Check if request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'disbursement_table.html', {'page_obj': page_obj})

    return render(request, 'apidata_view.html', {'page_obj': page_obj})

def input_form(request, disbursement_id):
    disbursement = get_object_or_404(DisbursementData, id=disbursement_id)

    if request.method == 'POST':
        form = InputWindowForm(request.POST)
        if form.is_valid():
            input_window = form.save(commit=False)
            input_window.disbursement = disbursement
            input_window.save()
            return redirect('view')  
    else:
        form = InputWindowForm()

    return render(request, 'input_form.html', {'form': form, 'disbursement': disbursement})


def view_input_detail(request, application_id):
    disbursement = get_object_or_404(DisbursementData, application_id=application_id)
    input_window = InputWindow.objects.filter(disbursement=disbursement).first()

    return render(request, 'input_detail.html', {
        'disbursement': disbursement,
        'input_window': input_window
    })

def output_form(request, disbursement_id):
    disbursement = get_object_or_404(DisbursementData, id=disbursement_id)
    disbursementdetail=get_object_or_404(DisbursementDetail,id=disbursement_id)
    inputwindow=get_object_or_404(InputWindow,id=disbursement_id)
    if request.method == 'POST':
        form = OutputDisForm(request.POST)
        if form.is_valid():
            output_window = form.save(commit=False)
            output_window.disbursement = disbursement
            output_window.application_id=disbursement.application_id
            output_window.refCode=disbursement.dsa_code
            output_window.franchCode=disbursement.fran_code
            output_window.disbursement_detail=disbursementdetail
            output_window.input_window=inputwindow
            output_window.save()
            return redirect('view') 
        else:
            print(form.errors) 
    else:
        form = OutputDisForm()

    return render(request, 'output_form.html', {'form': form, 'disbursement': disbursement})

def view_output_detail(request, application_id):
    disbursement = get_object_or_404(DisbursementData, application_id=application_id)
    output_window =Disbursement.objects.filter(disbursement=disbursement).first()

    return render(request, 'output_detail.html', {
        'disbursement': disbursement,
        'output_window': output_window
    })

def settle_form(request, disbursement_id):
    disbursement = get_object_or_404(DisbursementData, id=disbursement_id)

    if request.method == 'POST':
        form = SettlementForm(request.POST)
        if form.is_valid():
            settle_window = form.save(commit=False)
            settle_window.disbursement = disbursement
            settle_window.application_id=disbursement.application_id
            settle_window.refCode=disbursement.dsa_code
            settle_window.franchCode=disbursement.fran_code
            settle_window.save()
            return redirect('view')  
    else:
        form = SettlementForm()

    return render(request, 'settle_form.html', {'form': form, 'disbursement': disbursement})

def view_settle_detail(request, application_id):
    disbursement = get_object_or_404(DisbursementData, application_id=application_id)
    settle_window = SettlementWindow.objects.filter(disbursement=disbursement).first()

    dsa_data = None
    if settle_window and settle_window.refCode:
        dsa_api_url = f"{settings.SOURCE_PROJECT_URL}dsa/{settle_window.refCode}/"
        params = {'dsa_registerid': settle_window.franchCode}

        try:
            response = requests.get(dsa_api_url, params=params)
            if response.status_code == 200:
                dsa_data = response.json()
            else:
                print("Error fetching DSA data:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

    franchise_data = None
    if settle_window and settle_window.franchCode:
        branch_api_url = f"{settings.SOURCE_PROJECT_URL}branch/{settle_window.franchCode}/"
        params = {'franchise_id': settle_window.franchCode}

        try:
            response = requests.get(branch_api_url, params=params)
            if response.status_code == 200:
                franchise_data = response.json()
            else:
                print("Error fetching branch data:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

    return render(request, 'settle_detail.html', {
        'disbursement': disbursement,
        'settle_window': settle_window,
        'dsa_data': dsa_data,
        'franchise_data':franchise_data
    })



import requests
import json
from django.contrib import messages,auth
def login_check(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        if not employee_id or not password:
            messages.error(request, "Both employee ID and password are required.")
            return render(request, 'login.html')

        api_url = f"{settings.HR_SOURCE_URL}/api/ho/{employee_id}/loginCheck/"
        payload = {'password': password}

        try:
            # Send POST request to external API with JSON payload
            response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})

            # Check the raw response content and status code
            print(f"Raw Response: {response.text}")
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                response_data = response.json()
                request.session['employee_id'] = response_data['employee_id']
                request.session['username'] = response_data['username']
                request.session['email'] = response_data['email']
                return redirect('dash')
            elif response.status_code == 401:
                messages.error(request, "Invalid credentials")
            elif response.status_code == 404:
                messages.error(request, "Employee not found")
            else:
                messages.error(request, "An unexpected error occurred. Please try again later.")

        except requests.RequestException as e:
            messages.error(request, "Could not connect to login server. Please try again.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def dashboard(request):
    employee_id=request.session.get('employee_id')
    username=request.session.get('username')
    email=request.session.get('email')

    disbursementcount=Disbursement.objects.all().count()
    settlementcount=SettlementWindow.objects.all().count()
    dsa_amount = Disbursement.objects.aggregate(total_amount=Sum('dsa_payout_slab_in_Rs'))['total_amount'] or 0
    branch_amount = Disbursement.objects.aggregate(total_amount=Sum('branch_payout_slab_in_Rs'))['total_amount'] or 0
    total_amount=dsa_amount+branch_amount

    context={'disbursementcount':disbursementcount,'settlementcount':settlementcount,'dsa_amount':dsa_amount,'branch_amount':branch_amount,'employee_id':employee_id,'username':username,'email':email,'total_amount':total_amount}

    return render(request,'count.html',context)

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login_check')

