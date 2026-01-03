from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, EmployeeProfile


class CustomUserCreationForm(UserCreationForm):
    """Form for creating users in admin."""

    class Meta:
        model = User
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):
    """Form for updating users in admin."""

    class Meta:
        model = User
        fields = "__all__"


class EmployeeProfileInline(admin.StackedInline):
    """Inline profile editing within user admin."""

    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = "Employee Profile"
    fields = ("full_name", "email", "phone", "position", "salary", "join_date")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with employee profile inline."""

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = [EmployeeProfileInline]

    list_display = (
        "username",
        "get_full_name",
        "get_email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("username", "profile__full_name", "profile__email")
    ordering = ("-date_joined",)

    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined"), "classes": ("collapse",)},
        ),
    )

    add_fieldsets = (
        (
            "Create User Account",
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
                "description": "After creating the user, you must add employee profile information.",
            },
        ),
    )

    def get_full_name(self, obj):
        return obj.profile.full_name if hasattr(obj, "profile") else "-"

    get_full_name.short_description = "Full Name"

    def get_email(self, obj):
        return obj.profile.email if hasattr(obj, "profile") else "-"

    get_email.short_description = "Email"


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    """Separate admin for employee profiles if needed."""

    list_display = (
        "full_name",
        "email",
        "position",
        "salary",
        "join_date",
        "created_at",
    )
    list_filter = ("position", "join_date")
    search_fields = ("full_name", "email", "user__username")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("User Account", {"fields": ("user",)}),
        ("Personal Information", {"fields": ("full_name", "email", "phone")}),
        ("Employment Details", {"fields": ("position", "salary", "join_date")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
