import requests
from django.conf import settings
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log the request path
        print("Request Path:", request.path)

        # Fetch data from the API
        try:
            response = requests.get(
                f'{settings.SUPERADMIN_URL}/superadmin/app1/api/FranchiseMasterData_AppliViewsets/'
            )
            # Ensure valid JSON response
            if response.status_code in [200, 201]:
                result = response.json()
                request.session['masterData'] = result[0].get('MasterDataImage') if result else ""
            else:
                print(f"API Error: {response.status_code}")
                request.session['masterData'] = ""  # Default value if API fails
        except requests.exceptions.RequestException as e:
            print(f"API Request Exception: {e}")
            request.session['masterData'] = ""
        except ValueError:
            print("Invalid JSON response from API.")
            request.session['masterData'] = ""

        # Redirect logic for unverified users
        if not request.session.get('verified'):
            if request.path == '/franchise/Login' and request.method != 'POST':
                print("Redirecting to Login Page")
                request.session['indexPage'] = True
                return render(request, 'dsaLogin.html')

        # Handle specific allowed paths
        if request.GET.get('id') and request.path.startswith('/franchise/AllLoans'):
            return None  # Continue processing the request
        elif request.path.startswith('/franchise/api/'):
            return None  # Allow API paths

        # Handle other franchise paths
        if (request.path.startswith('/franchise/') or request.path.startswith('/franchisecomisions/')) and not request.session.get('verified') and request.path != '/franchise/Login':
            if request.session.get('indexPage'):
                del request.session['indexPage']
            request.session['pageurl'] = request.build_absolute_uri()
            return render(request, 'dsaLogin.html')

        # For all other cases, continue with the response
        return None
