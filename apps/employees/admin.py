from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "role", "phone", "join_date", "is_admin"]
    list_filter = ["role", "position", "join_date"]
    search_fields = ["name", "user__username", "phone", "position"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("User Information", {"fields": ("user", "name", "role")}),
        ("Contact Information", {"fields": ("phone", "address", "emergency_contact")}),
        ("Employment Details", {"fields": ("position", "salary", "join_date")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def is_admin(self, obj):
        return obj.is_admin

    is_admin.boolean = True
    is_admin.short_description = "Admin Status"
