# views.py

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
from .utils import get_api_count

@csrf_exempt
def hrLogin(request):
    errorMessage = None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        response = requests.get(f"{settings.SUPERADMIN_PROJECT_URL}/api/mymodel/None/{email}/{password}/hrLoginCheck/")
        if response.status_code == 200:
            # Store HR credentials if not already in the database
            HRcredentials.objects.get_or_create(email=email, defaults={'email': email})
            # Set the session variable with the email
            request.session['user_email'] = email
            return redirect('count')  # Redirect to dashboard
        else:
            errorMessage = "Wrong Credentials"
    return render(request, 'reg/loginhr.html', {'errorMessage': errorMessage})


# Generate employee ID
def generate_employee_id():
    last_employee = Employee.objects.order_by('id').last()
    if not last_employee:
        return 'SLNEMP1001'
    employee_id = last_employee.employee_id
    employee_number = int(employee_id.split('SLNEMP')[1])
    new_employee_id = f'SLNEMP{employee_number + 1:04d}'
    return new_employee_id

def register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.employee_id = generate_employee_id()  # Make sure this function generates an ID
            employee.save()

            # Get the necessary details
            employee_id = employee.employee_id
            password = form.cleaned_data['password']  # Assuming your form has a password field
            employee_type = employee.employee_type  # Adjust this if the employee type is stored differently
            franchisecode = employee.franchisecode

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('success', employee_id=employee_id, password=password, employee_type=employee_type)
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'reg/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            password = form.cleaned_data.get('password')

            # Authenticate the employee
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                if employee.check_password(password):
                    auth.login(request, employee)
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid employee ID or password.')
            except Employee.DoesNotExist:
                messages.error(request, 'Invalid employee ID or password.')

    else:
        form = EmployeeLoginForm()

    return render(request, 'reg/login.html', {'form': form})
def success(request, employee_id, password, employee_type):
    context = {
        'employee_id': employee_id,
        'password': password,
        'employee_type': employee_type,
    }
    return render(request, 'reg/success.html', context)

def dashboard(request):
    return render(request, 'reg/dashboard.html')

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('hrlogin')


   
import requests
from django.shortcuts import render
from django.http import HttpResponse

def hrdsaview(request):
    url = f"{settings.SOURCE_PROJECT_URL}dsaapi/"
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    print(data)

    for item in data:
        dsa_registerid = item.get('dsa_id')
        dsa_name = item.get('name')
        email = item.get('email')
        phone = item.get('phone')
        pan = item.get('pan')
        aadhar = item.get('aadhar')
        profession = item.get('profession')
        city = item.get('city')
        acc_number = item.get('acc_number')
        acc_holder_name = item.get('acc_holder_name')
        bank_name = item.get('bank_name')
        ifsc_code = item.get('ifsc_code')
        branch_name = item.get('branch_name')
        agreeCheck = item.get('agreeCheck')
   

        # Check if employee already exists, if so, update it; otherwise create a new entry
        employee, created = dsa.objects.update_or_create(
            dsa_registerid =  dsa_registerid,  # Use employee_id as the unique identifier
            defaults={
                'dsa_name': dsa_name,
                'email': email,
                'phone': phone,
                'pan': pan,
                'aadhar': aadhar,
                'profession': profession,
                'city': city,
                'acc_number': acc_number,
                'acc_holder_name': acc_holder_name,
                'bank_name': bank_name,
                'ifsc_code': ifsc_code,
                'branch_name': branch_name,
                'agreeCheck': agreeCheck,
            }   
        )

    branch = dsa.objects.all()
    return render(request, 'reg/hrdsaview.html', {'branch': branch})
         
def dsa_approve(request, employee_id):
    # Approve the franchise
    employee = get_object_or_404(dsa, id=employee_id)
    employee.approval_status = 'approved'
    employee.save()
    return redirect('dsapproved')
    
def approved(request):
    # Fetch only approved franchises
    approved_dsa = dsa.objects.filter(approval_status='approved')
    return render(request, 'reg/dsaapprove.html', {'approved_dsa': approved_dsa})

def dsa_reject(request, employee_id):
    # Reject the franchise
    employee = get_object_or_404(dsa, id=employee_id)
    employee.approval_status = 'rejected'
    employee.save()
    return redirect('dsa_rejected')

def dsa_rejected(request):
    # Fetch only rejected franchises
    rejected_dsa = dsa.objects.filter(approval_status='rejected')
    return render(request, 'reg/dsareject.html', {'rejected_dsa': rejected_dsa})

def approvedfranchises(request):
    # Construct the URL for fetching approved franchises
    url = f"{settings.SUPERADMIN_PROJECT_URL}superadmin/records/approverecords/"
    
    # Fetch the data from the external API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        approved_franchises = response.json()  # Parse JSON data
    except requests.exceptions.RequestException as e:
        # Handle any errors (e.g., network error, server error)
        print(f"Error fetching data: {e}")
        approved_franchises = []  # Fallback to an empty list in case of error

    # Render the template with the fetched data
    return render(request, 'reg/superadminapprove.html', {'approved_franchises':approved_franchises})



def hrfranchise_view(request):
        url = f"{settings.SOURCE_PROJECT_URL}franchise_api/"
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Check if the request was successful
        
        data = response.json()
        print(data)

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

            # Check if franchise already exists, if so, update it; otherwise create a new entry
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
        
        branch=franchise.objects.all()
        return render(request, 'reg/hrfranchise.html', {'branch': branch})
            
        #     # Assuming dsaPhoto, aadharFront, aadharBack, panCard, and bankDocument are in base64 format
            
def approve_employee(request, employee_id):
    # Approve the franchise
    employee = get_object_or_404(franchise, id=employee_id)
    employee.aproval_status = 'approved'
    employee.save()
    return redirect('approved_franchises')

def approved_franchises(request):
    # Fetch only approved franchises
    approved_franchises = franchise.objects.filter(aproval_status='approved')
    return render(request, 'reg/approve.html', {'approved_franchises': approved_franchises})  
    

def reject_employee(request, employee_id):
    # Fetch only rejected franchises
    employee = get_object_or_404(franchise, id=employee_id)
    employee.aproval_status = 'rejected'
    employee.save()
    return redirect('rejected_franchises')

def rejected_franchises(request):
    # Reject the franchise
    approved_franchises = franchise.objects.filter(aproval_status='rejected')
    return render(request, 'reg/reject.html', {'approved_franchises': approved_franchises}) 

      

import logging

logger = logging.getLogger(__name__)

def hrEduViewsets(request):
     return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}el/loan-records/"})

def hrgoldapi(request):
      return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}goldview/"})


from django.conf import settings
def hrplapi(request):
  return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}pl/personallist/"})

def hrlapapi(request):
     return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}lapview/"})

def hrhlapi(request):
      return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}pl/homelist/"})

def hrBusiViewsets(request):
     return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}bl/business-loans-lists"})


def hrddproject(request):
     return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}cl/car-loans-list/"})

def hrapi_credit_appli(request):
   return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}cc/table_view/"})

def hrotherapi(request):
    return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}otherview/"})


def hrviewinsurance(request):
    return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewinsurance/"})

def hrviewlifeinsurance(request):
    return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewlifeinsurance/"})

def hrviewhealthinsurance(request):
    return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewhealthinsurance/"})
def hrviewgeninsurance(request):
    return render(request,"reg/hrpl.html",{'url':f"{settings.SOURCE_PROJECT_URL}viewgeninsurance/"})

    

def lists(request, employee_id):
    # Get the logged-in employee
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        # Handle the case where employee does not exist
        return redirect('some_error_page')

    # Initialize the form
    form = franchisesalesForm(request.POST or None)

    # Get all franchise sales records for display
    franchise_sales_data = franchisesales.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            franchise_sale = form.save(commit=False)
            franchise_sale.Employe = employee  # Link to the current employee
            
            # Check if conditions are met to set franchiseCode automatically
            if employee.franchisecode == 'SLNBR001' and employee.employee_type == 'sales':
                franchise_sale.franchiseCode = employee.franchisecode
            
            # Save the form data to the database
            franchise_sale.save()
            return redirect('create_and_display_franchise_sales')  # Reload the page
        else:
            print(form.errors)  # Debugging: print form errors if any

    # Pass the form, employee, and all franchise sales data to the template
    context = {
        'form': form,
        'employee': employee,
        'franchise_sales_data': franchise_sales_data,
    }
    return render(request, 'franchise_sales.html', context)


# ==========================register===========================

# ==========================register===========================

from django.shortcuts import redirect, get_object_or_404
from .models import dsa


def register_sales(request):
    if request.method == 'POST':
        form = SalesRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('okkk')
    else:
        form = SalesRegistrationForm()
    return render(request, 'reg/register_sales.html', {'form': form})

def register_dsa_user(request):
    if request.method == 'POST':
        form = DSAUsersRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('okkk')
    else:
        form = DSAUsersRegistrationForm()
    return render(request, 'reg/register_dsa_user.html', {'form': form})

def register_franchise_user(request):
    if request.method == 'POST':
        form = FranchiseUsersRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('okkk')
    else:
        form = FranchiseUsersRegistrationForm()
    return render(request, 'reg/register_franchise_user.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('okkk')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'reg/register_customer.html', {'form': form})


# ========================lists===============================



def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'reg/employee_list.html', {'employees': employees})

def dsa_list(request):
    dsas = DSAUsers.objects.all()
    return render(request, 'reg/dsa_list.html', {'dsas': dsas})

def sales_list(request):
    sales = Sales.objects.all()
    return render(request, 'reg/sales_list.html', {'sales': sales})

def franchise_list(request):
    franchises = FranchiseUsers.objects.all()
    return render(request, 'reg/franchise_list.html', {'franchises':franchises})

def hr_dashboard_view(request):
    email = request.session.get('user_email')
    edu_records_url = f"{settings.SOURCE_PROJECT_URL}el/loan-records/"
    gold_records_url = f"{settings.SOURCE_PROJECT_URL}goldview/"
    personal=f"{settings.SOURCE_PROJECT_URL}pl/personallist/"
    lap=f"{settings.SOURCE_PROJECT_URL}lapview/"
    home=f"{settings.SOURCE_PROJECT_URL}pl/homelist/"
    bus=f"{settings.SOURCE_PROJECT_URL}bl/business-loans-lists"
    car=f"{settings.SOURCE_PROJECT_URL}cl/car-loans-list/"
    cc=f"{settings.SOURCE_PROJECT_URL}cc/table_view/"
    other=f"{settings.SOURCE_PROJECT_URL}otherview/"
    viewins=f"{settings.SOURCE_PROJECT_URL}viewinsurance/"
    viewlife=f"{settings.SOURCE_PROJECT_URL}viewlifeinsurance/"
    viewhel=f"{settings.SOURCE_PROJECT_URL}viewhealthinsurance/"
    viewgen=f"{settings.SOURCE_PROJECT_URL}viewgeninsurance/"
    total_loans_count=get_api_count(edu_records_url+gold_records_url+personal+lap+home+bus+car+other)
    total_ins_count=get_api_count(viewins+viewlife+viewgen+viewhel)
    #branchoffice
    loan_backend=Employee.objects.filter(employee_type='Backendemployee').count()
    accounts_count=Employee.objects.filter(employee_type='Accounts').count()
    customer_support_count=Employee.objects.filter(employee_type='customersupport').count()
    ho_sales_count=Sales.objects.filter(franchiseCode='SLNBR001').count()
    ho_dsa_count=DSAUsers.objects.filter(franchiseCode='SLNBR001').count()
    #--------end--------
    franchise_count = franchise.objects.count()
    approved_franchises_count = franchise.objects.filter(aproval_status='approved').count()
    rejected_franchises_count = franchise.objects.filter(aproval_status='rejected').count()
    dsa_count = dsa.objects.count()
    approved_dsa_count = dsa.objects.filter(approval_status='approved').count()
    rejected_dsa_count = dsa.objects.filter(approval_status='rejected').count()

    sales_count = Sales.objects.exclude(franchiseCode='SLNBR001').count()

    dsausers_count = DSAUsers.objects.exclude(franchiseCode='SLNBR001').count()
    total_employee_count=loan_backend+accounts_count+customer_support_count+ho_sales_count+ ho_dsa_count

    edu_records_url = get_api_count(edu_records_url)
    gold_records_url = get_api_count(gold_records_url)
    personal=get_api_count(personal)
    lap=get_api_count(lap)
    home=get_api_count(home)
    bus=get_api_count(bus)
    car=get_api_count(car)
    cc=get_api_count(cc)
    other=get_api_count(other)
    viewins=get_api_count(viewins)
    viewlife=get_api_count(viewlife)
    viewhel=get_api_count(viewhel)
    viewgen=get_api_count(viewgen)
    context = {
        
        'total_employee_count':total_employee_count,
        'loan_backend':loan_backend,
        'accounts_count':accounts_count,
        'customer_support_count':customer_support_count,
        'ho_sales_count':ho_sales_count,
        'ho_dsa_count':ho_dsa_count,
        'franchise_count': franchise_count,
        'approved_franchises_count': approved_franchises_count,
        'rejected_franchises_count': rejected_franchises_count,
        'dsa_count': dsa_count,
        'approved_dsa_count': approved_dsa_count,
        'rejected_dsa_count': rejected_dsa_count,
        'sales_count': sales_count,
        'dsausers_count':dsausers_count,
        'edu_records_url': edu_records_url,
        'gold_records_url': gold_records_url,
        'personal':personal,
        'home':home,
        'lap':lap,
        'bus':bus,
        'cc':cc,
        'car':car,
        'other':other,
        'viewins':viewins,
        'viewlife':viewlife,
        'viewhel':viewhel,
        'viewgen':viewgen,
        'total_loans_count':total_loans_count,
        'total_ins_count':total_ins_count,
        'user_email': email,   
        

    }

    return render(request, 'reg/count.html', context)

