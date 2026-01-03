from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, LogoutView, ProfileView, VerifyTokenView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("verify/", VerifyTokenView.as_view(), name="verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
