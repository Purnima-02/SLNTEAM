from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class EmployeeLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        is_authenticated = request.session.get('employee_id') is not None

        if not is_authenticated:
            if request.path != reverse('login_check'): 
                return redirect(reverse('login_check'))
        
        if is_authenticated and request.path == reverse('login_check'):
            return redirect(reverse('dashboard'))  
