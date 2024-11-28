from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class EmployeeLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Only apply this middleware to URLs that start with 'emp'
        if request.path.startswith('/manager/'):
            # Check if the user is authenticated by verifying if 'employee_id' exists in the session
            is_authenticated = request.session.get('user_email') is not None

            # If the user is not authenticated, redirect them to the login page
            if not is_authenticated:
                if request.path != reverse('hrlogin'):  # Assuming 'login_check' is the URL name for 'login/check/'
                    return redirect(reverse('hrlogin'))
            
            # If the user is authenticated and tries to access the login page, redirect to the dashboard
            if is_authenticated and request.path == reverse('hrlogin'):
                return redirect(reverse('count'))
    