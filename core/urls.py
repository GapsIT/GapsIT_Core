from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.employees.views import CustomTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication endpoints
    path(
        "api/auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Employee endpoints
    path("api/", include("apps.employees.urls")),
]
