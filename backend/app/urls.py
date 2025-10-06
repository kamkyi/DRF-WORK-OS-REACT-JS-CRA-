from django.urls import path
from .views import WorkOSAuthCallbackView, LogoutView, ProtectedHelloView

urlpatterns = [
    path(
        "auth/workos/callback", WorkOSAuthCallbackView.as_view(), name="workos-callback"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("hello", ProtectedHelloView.as_view(), name="hello"),
]
