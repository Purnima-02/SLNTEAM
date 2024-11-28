from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
import logging
from django.contrib import messages
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from requests.exceptions import JSONDecodeError


 





logger = logging.getLogger(__name__)

def create_ticket(request, instance_id=None):
    # Fetch the Ticket object if an instance_id is provided
    customer_profile = get_object_or_404(Ticket, id=instance_id) if instance_id else None

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            customer_profile = form.save()
            return redirect('ok')  # Adjust if you have a specific URL name for success
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = TicketForm(instance=customer_profile)

    random_number = customer_profile.random_number if customer_profile else None

    # Fetch open tickets. Filter by random_number if provided.
    if random_number:
        open_tickets = Ticket.objects.filter(random_number=random_number, status='open')
    else:
        open_tickets = Ticket.objects.filter(status='open')

    return render(request, 'create_ticket.html', {
        'form': form,
        'random_number': random_number,
        'open_tickets': open_tickets
    })



def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket.status = status
        ticket.save()
        return redirect('new_dashboard')
    return render(request, 'update_ticket_status.html', {'ticket': ticket})


def ticket_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket.status = status
        ticket.save()
        return redirect('ticketview')
    return render(request, 'ticket_details.html', {'ticket': ticket})



@csrf_exempt
def customerLogin(request):
    errorMessage = None
    
    if request.method == "POST":
        id = request.POST.get('name')
        passw = request.POST.get('password')
        

        # Construct the URL
        login_url = f"{settings.HR_SOURCE_URL}/api/mymodel/{id}/{passw}/customerLoginCheck/"

        try:
            response = requests.get(login_url)
            response.raise_for_status()  # Raise an error for bad responses

            if response.status_code == 200:
                res = response.json()

                # Check if response has the expected data
                if res and isinstance(res, list) and len(res) > 0:
                    franchise_code = res[0].get('franchiseCode')  
                    if franchise_code:
                        custmer.objects.get_or_create(name=id, defaults={'name': id})
                        request.session['verified'] = True
                        request.session['name'] = id
                        request.session['franchCode'] = franchise_code

                        if request.session.get('indexPage'):
                            return redirect('newdashboard')
                        
                        return redirect(request.session.get('pageurl'))
                    else:
                        errorMessage = "Franchise code not found in the response."
                else:
                    errorMessage = "Invalid response structure from the authentication service."
            else:
                errorMessage = "Wrong Credentials"

        except requests.exceptions.RequestException as e:
            errorMessage = "Could not connect to the authentication service."

    return render(request, 'login.html', {'errorMessage': errorMessage})




def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout



def ticketview(request):
     data=Ticket.objects.all()
     return render(request,'ticket_view.html',{'data':data})



def ok(request):
    return render(request,'ok.html')




def open_tickets_view(request):
    open_tickets = Ticket.objects.filter(status='open')
    return render(request, 'open_tickets.html', {'open_tickets': open_tickets})



def inprogress_tickets_view(request):
    in_progress_tickets = Ticket.objects.filter(status='in_progress')
    return render(request, 'inprogress_tickets.html', {'in_progress_tickets': in_progress_tickets})



def resolved_tickets(request):
    resolved_tickets = Ticket.objects.filter(status='resolved')
    return render(request, 'resolved_tickets.html', {'resolved_tickets': resolved_tickets})






# ///////////////////////       DSA       //////////////////////////////////////





def DSA_create_ticket(request, instance_id=None):
    # Fetch the Ticket object if an instance_id is provided
    customer_profile = get_object_or_404(DSATicket, id=instance_id) if instance_id else None

    if request.method == 'POST':
        form = DSATicketForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            customer_profile = form.save()
            return redirect('ok')  # Adjust if you have a specific URL name for success
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = DSATicketForm(instance=customer_profile)

    random_number = customer_profile.random_number if customer_profile else None

    # Fetch open tickets. Filter by random_number if provided.
    if random_number:
        open_tickets = DSATicket.objects.filter(random_number=random_number, status='open')
    else:
        open_tickets = DSATicket.objects.filter(status='open')

    return render(request, 'DSA/DSAticket_form.html', {
        'form': form,
        'random_number': random_number,
        'open_tickets': open_tickets
    })



def DSA_update_ticket_status(request, ticket_id):
    DSA_ticket = get_object_or_404(DSATicket, pk=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        DSA_ticket.status = status
        DSA_ticket.save()
        return redirect('new_dashboard')
    return render(request, 'DSA/DSA_update_ticket.html', {'DSA_ticket': DSA_ticket})


def DSA_ticket_details(request, ticket_id):
    DSA_ticket = get_object_or_404(DSATicket, pk=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        DSA_ticket.status = status
        DSA_ticket.save()
        return redirect('DSA_ticketview')
    return render(request, 'DSA/DSA_ticket_details.html', {'DSA_ticket': DSA_ticket})


def DSA_ticketview(request):
     DSA_data=DSATicket.objects.all()
     return render(request,'DSA/DSA_tickets_view.html',{'DSA_data':DSA_data})


def DSA_open_tickets_view(request):
    DSA_open_tickets = DSATicket.objects.filter(status='open')
    return render(request, 'DSA/DSA_open_tickets.html', {'DSA_open_tickets': DSA_open_tickets})



def DSA_inprogress_tickets_view(request):
    DSA_in_progress_tickets = DSATicket.objects.filter(status='in_progress')
    return render(request, 'DSA/DSA_inprogress_tickets.html', {'DSA_in_progress_tickets': DSA_in_progress_tickets})



def DSA_resolved_tickets(request):
    DSA_resolved_tickets = DSATicket.objects.filter(status='resolved')
    return render(request, 'DSA/DSA_resolved_tickets.html', {'DSA_resolved_tickets': DSA_resolved_tickets})



 # ///////////////////////////////////////   Franchisee   /////////////////////////////////

 
def Franchisee_create_ticket(request, instance_id=None):
    # Fetch the Ticket object if an instance_id is provided
    customer_profile = get_object_or_404(FranchiseeTicket, id=instance_id) if instance_id else None

    if request.method == 'POST':
        form = FranchiseeTicketForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            customer_profile = form.save()
            return redirect('ok')  # Adjust if you have a specific URL name for success
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = FranchiseeTicketForm(instance=customer_profile)

    random_number = customer_profile.random_number if customer_profile else None

    # Fetch open tickets. Filter by random_number if provided.
    if random_number:
        open_tickets = FranchiseeTicket.objects.filter(random_number=random_number, status='open')
    else:
        open_tickets = FranchiseeTicket.objects.filter(status='open')

    return render(request, 'franchisee/fran_ticketform.html', {
        'form': form,
        'random_number': random_number,
        'open_tickets': open_tickets
    })



def Franchisee_update_ticket_status(request, ticket_id):
    frachisee_ticket = get_object_or_404(FranchiseeTicket, pk=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        frachisee_ticket.status = status
        frachisee_ticket.save()
        return redirect('new_dashboard')
    return render(request, 'franchisee/fan_updateticket.html', {'frachisee_ticket': frachisee_ticket})


def Franchisee_ticket_details(request, ticket_id):
    franchisee_ticket = get_object_or_404(FranchiseeTicket, pk=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        franchisee_ticket.status = status
        franchisee_ticket.save()
        return redirect('DSA_ticketview')
    return render(request, 'franchisee/fran_ticketdetails.html', {'franchisee_ticket': franchisee_ticket})


def Franchisee_ticketview(request):
     franchisee_data=FranchiseeTicket.objects.all()
     return render(request,'franchisee/fran_viewticket.html',{'franchisee_data':franchisee_data})


def Franchisee_open_tickets_view(request):
    franchisee_open_tickets = FranchiseeTicket.objects.filter(status='open')
    return render(request, 'franchisee/fran_open_ticket.html', {'franchisee_open_tickets': franchisee_open_tickets})



def Franchisee_inprogress_tickets_view(request):
    franchisee_in_progress_tickets = FranchiseeTicket.objects.filter(status='in_progress')
    return render(request, 'franchisee/fran_inprogress_ticketst.html', {'franchisee_in_progress_tickets': franchisee_in_progress_tickets})



def Franchisee_resolved_tickets(request):
    franchisee_resolved_tickets = FranchiseeTicket.objects.filter(status='resolved')
    return render(request, 'franchisee/fran_resolved_tickets.html', {'franchisee_resolved_tickets': franchisee_resolved_tickets})







# ////////////////////////////////     dashboard       ///////////////////////////////////////


    

def newdash(request):
    total_tickets = Ticket.objects.count()
    total_dsa_tickets = DSATicket.objects.count()
    total_Franchisee_tickets = FranchiseeTicket.objects.count()
   
    return render(request, 'DSA/newdashboard.html', {
        'total_tickets': total_tickets,
        'total_dsa_tickets': total_dsa_tickets, 
        'total_Franchisee_tickets': total_Franchisee_tickets,
        


        'user': request.user
   
    })
     
def Customer_tickets(request):
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()
    in_progress_tickets = Ticket.objects.filter(status='in_progress').count()
    resolved_tickets = Ticket.objects.filter(status='resolved').count()

    return render(request, 'dashboard/customer_support.html',{
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,

    })



     
def DSA_tickets(request):
    total_dsa_tickets = DSATicket.objects.count()
    dsa_open_tickets = DSATicket.objects.filter(status='open').count()
    dsa_in_progress_tickets = DSATicket.objects.filter(status='in_progress').count()
    dsa_resolved_tickets = DSATicket.objects.filter(status='resolved').count()

    return render(request, 'dashboard/DSA_support.html',{
        'total_dsa_tickets': total_dsa_tickets,
        'dsa_open_tickets': dsa_open_tickets,
        'dsa_in_progress_tickets': dsa_in_progress_tickets,
        'dsa_resolved_tickets': dsa_resolved_tickets,

    })


def Franchisee_tickets(request):   
    total_Franchisee_tickets = FranchiseeTicket.objects.count()
    Franchisee_open_tickets = FranchiseeTicket.objects.filter(status='open').count()
    Franchisee_in_progress_tickets = FranchiseeTicket.objects.filter(status='in_progress').count()
    Franchisee_resolved_tickets = FranchiseeTicket.objects.filter(status='resolved').count()
    
    return render(request, 'dashboard/franchisee_support.html',{
       'total_Franchisee_tickets': total_Franchisee_tickets,
        'Franchisee_open_tickets': Franchisee_open_tickets,
        'Franchisee_in_progress_tickets': Franchisee_in_progress_tickets,
        'Franchisee_resolved_tickets': Franchisee_resolved_tickets,


    })


def dash(request):
        employee_id=request.session.get('employee_id')
        user_name=request.session.get('username')
        email=request.session.get('email')
        return render(request, 'dashboard.html',{'employee_id':employee_id,'username':user_name,'email':email})


# Create your views here.
def contactsupport(request):
  return render(request,"contact.html",{'url':f"{settings.SOURCE_PROJECT_URL}/contact-submissions/"})



def login_check(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        
        api_url = f"{settings.HR_SOURCE_URL}/employee/{employee_id}/loginCheck/"
        
        try:
            response = requests.get(api_url, params={'password': password})
            
            if response.status_code == 200:
                employee_data = response.json()
                request.session['employee_id'] = employee_data['employee_id']  
                # request.session['username'] = employee_data['username']  
                request.session['username']=employee_data.get('username')
                request.session['employee_id']=employee_data.get('employee_id')
                request.session['email']=employee_data.get('email')

                return redirect('dashboard')
            elif response.status_code == 401:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
            elif response.status_code == 404:
                return render(request, 'login.html', {'error_message': 'Employee not found'})
            else:
                return render(request, 'login.html', {'error_message': 'User Already exist'})
        
        except requests.RequestException:
            return render(request, 'login.html', {'error_message': 'Could not connect to login server'})
    
    return render(request,'login.html')



def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login_check')