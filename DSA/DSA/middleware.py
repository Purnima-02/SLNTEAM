# myapp/middleware.py

from django.conf import settings
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
import requests
from requests.exceptions import JSONDecodeError


class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware Triggered for Path:", request.path)

        # Fetch Master Data from the external API
        try:
            response = requests.get(
                f"{settings.SUPERADMIN_URL}/superadmin/app1/api/DSAMasterData_AppliViewsets/"
            )
            if response.status_code in [200, 201]:
                result = response.json()
                result = result[0] if result else None
                request.session["masterData"] = result.get("MasterDataImage") if result else ""
            else:
                request.session["masterData"] = ""
        except (requests.RequestException, JSONDecodeError) as e:
            print(f"Error fetching master data: {e}")
            request.session["masterData"] = ""

        # Handle specific paths and conditions
        if (
            not request.session.get("verified")
            and request.path == "/dsa/dsaLogin"
            and request.method != "POST"
        ):
            print("Redirecting to dsaLogin")
            request.session["indexPage"] = True
            return render(request, "dsaLogin.html")

        if request.GET.get("id") and request.path.startswith("/dsa/AllLoans"):
            request.session["dsanologin"] = True
            return self.get_response(request)

        if request.path.startswith("/dsa/api/"):
            return self.get_response(request)

        if (
            (request.path.startswith("/dsa/") or request.path.startswith("/dsacomisions/"))
            and not request.session.get("verified")
            and request.path != "/dsa/dsaLogin"
        ):
            if request.session.get("indexPage"):
                del request.session["indexPage"]
            request.session["pageurl"] = request.build_absolute_uri()
            return render(request, "dsaLogin.html")

        # Default response for other paths
        response = self.get_response(request)
        return response

