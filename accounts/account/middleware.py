from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import requests

class EmployeeLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the user is authenticated by verifying if 'employee_id' exists in the session
        is_authenticated = request.session.get('employee_id') is not None

        # If the user is not authenticated, redirect them to the login page
        if not is_authenticated:
            if request.path != reverse('login_check'):  # Assuming 'login_check' is the URL name for 'login/check/'
                return redirect(reverse('login_check'))
        
        # If the user is authenticated and tries to access the login page, redirect to the dashboard
        if is_authenticated and request.path == reverse('login_check'):
                return redirect(reverse('dash'))  # Assuming 'dash' is the URL name for the dashboard


import requests
from json.decoder import JSONDecodeError

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        print("Im Middleware")
        try:
            # Make the API request
            response = requests.get(f'{settings.SUPERADMIN_URL}superadmin/app1/api/AccountsMasterData_AppliViewsets/')
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

            # Try to parse the JSON response
            result = response.json()
            result = result[0] if result else None
            request.session['masterData'] = result.get('MasterDataImage') if result else ""

        except JSONDecodeError:
            print("JSONDecodeError: Invalid JSON response from the API.")
            request.session['masterData'] = None
        except requests.exceptions.RequestException as e:
            print(f"RequestException: {e}")
            request.session['masterData'] = None

        return self.get_response(request)
        
