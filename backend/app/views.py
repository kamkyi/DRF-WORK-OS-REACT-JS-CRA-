import os
import requests
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
import workos
from workos import user_management

WORKOS_API_KEY = os.getenv("WORKOS_API_KEY")
WORKOS_CLIENT_ID = os.getenv("WORKOS_CLIENT_ID")
WORKOS_REDIRECT_URI = os.getenv("WORKOS_REDIRECT_URI")
WORKOS_COOKIE_PASSWORD = os.getenv("WORKOS_COOKIE_PASSWORD")

# Configure WorkOS
workos.api_key = WORKOS_API_KEY


def mint_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class WorkOSAuthCallbackView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Handle GET request from WorkOS redirect with code in query parameters.
        """
        code = request.GET.get("code")
        id_token = request.GET.get("id_token")
        return self._handle_auth(code, id_token)

    def post(self, request):
        """
        Accept either:
          - {"code": "<oauth_code>"}  (preferred server-side exchange)
          - {"id_token": "<id_token>"} (fallback if you use implicit)
        Returns your app JWT tokens {access, refresh}.
        """
        code = request.data.get("code")
        id_token = request.data.get("id_token")
        return self._handle_auth(code, id_token)

    def _handle_auth(self, code, id_token):
        """
        Common authentication handler for both GET and POST requests.
        """
        try:
            if code:
                # Server-side exchange using WorkOS REST API
                auth_url = "https://api.workos.com/user_management/authenticate"
                auth_payload = {
                    "client_id": WORKOS_CLIENT_ID,
                    "client_secret": WORKOS_API_KEY,
                    "grant_type": "authorization_code",
                    "code": code,
                }

                auth_response = requests.post(auth_url, json=auth_payload)

                if auth_response.status_code != 200:
                    return Response(
                        {
                            "error": "WorkOS authentication failed",
                            "detail": auth_response.text,
                        },
                        status=400,
                    )

                auth_data = auth_response.json()
                user_info = auth_data.get("user", {})
                email = user_info.get("email")
                first_name = user_info.get("first_name") or ""
                last_name = user_info.get("last_name") or ""
                external_id = user_info.get("id")  # WorkOS user id
            elif id_token:
                # Handle id_token verification (not commonly used)
                return Response(
                    {"error": "ID token authentication not implemented"}, status=400
                )
            else:
                return Response({"error": "Missing code or id_token"}, status=400)

            if not email:
                return Response({"error": "No email returned from AuthKit"}, status=400)

            # Upsert local user
            user, _created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            # Optional: keep names fresh
            updated = False
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if user.last_name != last_name:
                user.last_name = last_name
                updated = True
            if updated:
                user.save(update_fields=["first_name", "last_name"])

            tokens = mint_tokens_for_user(user)
            return Response(
                {
                    "user": {
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "workos_id": external_id,
                    },
                    **tokens,
                }
            )
        except Exception as e:
            return Response(
                {"error": "AuthKit exchange failed", "detail": str(e)}, status=400
            )


class WorkOSLogoutView(APIView):
    """
    Handle logout flow with WorkOS AuthKit.
    Clears the sealed session cookie and redirects to WorkOS logout URL.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Handle logout request:
        1. Load the sealed session from WorkOS cookie
        2. Get logout URL from WorkOS
        3. Clear the WorkOS session cookie
        4. Redirect to WorkOS logout URL
        """
        try:
            # Get the WorkOS session cookie
            wos_session_cookie = request.COOKIES.get("wos_session")

            if wos_session_cookie and WORKOS_COOKIE_PASSWORD:
                try:
                    # Load the sealed session using WorkOS
                    session = workos.user_management.load_sealed_session(
                        session_data=wos_session_cookie,
                        cookie_password=WORKOS_COOKIE_PASSWORD,
                    )

                    # Get the WorkOS logout URL
                    logout_url = session.get_logout_url()

                    # Create redirect response to WorkOS logout
                    response = HttpResponseRedirect(logout_url)

                    # Clear the WorkOS session cookie
                    response.delete_cookie(
                        "wos_session",
                        path="/",
                        domain=None,  # Use same domain as when cookie was set
                        samesite="Lax",
                    )

                    return response

                except Exception as session_error:
                    # If session loading fails, still clear cookie and redirect
                    print(f"Session loading error: {session_error}")

            # Fallback: redirect to login if no session or session loading failed
            # You can customize this URL to match your frontend login page
            fallback_url = f"{request.scheme}://{request.get_host()}/login"
            response = HttpResponseRedirect(fallback_url)

            # Clear any WorkOS session cookie even if we couldn't load it
            response.delete_cookie("wos_session", path="/")

            return response

        except Exception as e:
            # If everything fails, return JSON error response
            return Response({"error": "Logout failed", "detail": str(e)}, status=500)

    def post(self, request):
        """
        Handle AJAX logout request - returns JSON instead of redirect.
        Useful for SPA applications that want to handle the redirect themselves.
        """
        try:
            wos_session_cookie = request.COOKIES.get("wos_session")
            logout_url = None

            if wos_session_cookie and WORKOS_COOKIE_PASSWORD:
                try:
                    # Load the sealed session using WorkOS
                    session = workos.user_management.load_sealed_session(
                        session_data=wos_session_cookie,
                        cookie_password=WORKOS_COOKIE_PASSWORD,
                    )

                    # Get the WorkOS logout URL
                    logout_url = session.get_logout_url()

                except Exception as session_error:
                    print(f"Session loading error: {session_error}")

            # Create JSON response with logout URL
            response_data = {
                "success": True,
                "logout_url": logout_url,
                "message": "Logged out successfully",
            }

            response = Response(response_data, status=200)

            # Clear the WorkOS session cookie
            response.delete_cookie("wos_session", path="/")

            return response

        except Exception as e:
            return Response({"error": "Logout failed", "detail": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    """
    WorkOS AuthKit Logout View
    Handles secure logout by clearing WorkOS session and redirecting to WorkOS logout URL
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Handle logout request:
        1. Load sealed session from wos_session cookie
        2. Get WorkOS logout URL from session
        3. Clear the wos_session cookie
        4. Redirect to WorkOS logout URL
        """
        try:
            # Step 1: Get the sealed session from cookie
            sealed_session = request.COOKIES.get("wos_session")

            if not sealed_session:
                # No session cookie found - return login URL
                return Response(
                    {"logout_url": "/login", "message": "No active session found"},
                    status=200,
                )

            # Step 2: Load the WorkOS session using the sealed session data
            cookie_password = os.getenv("WORKOS_COOKIE_PASSWORD")
            if not cookie_password:
                return Response(
                    {"error": "WORKOS_COOKIE_PASSWORD not configured"}, status=500
                )

            try:
                # Load sealed session using WorkOS user management
                session = user_management.load_sealed_session(
                    sealed_session, cookie_password=cookie_password
                )

                # Step 3: Get the logout URL from WorkOS session
                logout_url = session.get_logout_url()

            except Exception as session_error:
                # If session loading fails, redirect to login as fallback
                print(f"Session loading error: {session_error}")
                logout_url = "/login"

            # Step 4: Create JSON response with logout URL for frontend to handle
            response_data = {"logout_url": logout_url, "message": "Logout successful"}
            response = Response(response_data, status=200)

            # Step 5: Delete the wos_session cookie to clear local session
            response.delete_cookie(
                "wos_session",
                path="/",
                domain=None,  # Uses same domain as when cookie was set
                samesite="Lax",
            )

            return response

        except Exception as e:
            # If anything fails, return error response
            return Response({"error": "Logout failed", "detail": str(e)}, status=500)


class ProtectedHelloView(APIView):
    """
    Example protected endpoint using your app JWT.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(
            {
                "message": f"Hello {request.user.username}! Time: {timezone.now().isoformat()}"
            }
        )
