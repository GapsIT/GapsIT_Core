from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Employee
from .serializers import (
    EmployeeSerializer,
    EmployeeListSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
)
from .permissions import IsAdmin, IsOwnerOrAdmin, HasAdminAPIKey


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that includes role in JWT and response"""

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get the user from request
            from rest_framework_simplejwt.tokens import RefreshToken
            from django.contrib.auth import authenticate

            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                try:
                    employee = user.employee
                    response.data["role"] = employee.role
                    response.data["name"] = employee.name
                    response.data["is_admin"] = employee.is_admin
                except Employee.DoesNotExist:
                    response.data["role"] = "employee"
                    response.data["name"] = user.username
                    response.data["is_admin"] = user.is_staff or user.is_superuser

        return response


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations

    Endpoints:
    - GET /api/employees/ - List all employees (admin only)
    - POST /api/employees/ - Create new employee (admin only)
    - GET /api/employees/{id}/ - Retrieve employee (owner or admin)
    - PUT/PATCH /api/employees/{id}/ - Update employee (owner or admin)
    - DELETE /api/employees/{id}/ - Delete employee (admin only)
    - GET /api/employees/me/ - Get current user's employee info
    - POST /api/employees/change_password/ - Change password
    - POST /api/employees/verify_admin/ - Verify admin status (with API key)
    """

    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        return EmployeeSerializer

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ["create", "destroy", "list"]:
            # Only admins can create, delete, or list all
            permission_classes = [IsAuthenticated, IsAdmin]
        elif self.action in ["update", "partial_update", "retrieve"]:
            # Owner or admin can update/view
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        elif self.action == "verify_admin":
            # Requires API key
            permission_classes = [HasAdminAPIKey]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current authenticated user's employee information"""
        try:
            employee = request.user.employee
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def change_password(self, request):
        """Change current user's password"""
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[HasAdminAPIKey])
    def verify_admin(self, request):
        """
        Verify admin status for external services
        Requires X-API-Key header with valid admin API key

        Request body:
        {
            "user_id": 1  // or "username": "john"
        }

        Response:
        {
            "is_admin": true,
            "user_id": 1,
            "username": "john",
            "role": "admin",
            "name": "John Doe"
        }
        """
        user_id = request.data.get("user_id")
        username = request.data.get("username")

        if not user_id and not username:
            return Response(
                {"error": "user_id or username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if user_id:
                employee = Employee.objects.get(user_id=user_id)
            else:
                employee = Employee.objects.get(user__username=username)

            return Response(
                {
                    "is_admin": employee.is_admin,
                    "user_id": employee.user.id,
                    "username": employee.user.username,
                    "role": employee.role,
                    "name": employee.name,
                }
            )
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )
