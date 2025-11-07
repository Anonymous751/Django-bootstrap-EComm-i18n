from django.contrib import admin
from apps.accounts.models import CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "analytics_level",   # ← ADDED HERE
        "is_active",
        "is_staff",
        "is_private",
        "is_blocked",
        "two_factor_enabled",
        "dark_mode",
    )

    list_editable = (
        "is_private",
        "is_blocked",
        "two_factor_enabled",
        "dark_mode",
    )

    list_filter = (
        "role",
        "analytics_level",   # ← ADDED HERE
        "is_active",
        "two_factor_enabled",
        "is_private",
        "is_blocked",
        "dark_mode",
    )

    search_fields = ("username", "email")

    fieldsets = (
        (None, {
            "fields": ("username", "email", "password")
        }),
        ("Personal info", {
            "fields": (
                "display_name",
                "profile_image",
                "bio",
                "location",
                "date_of_birth"
            )
        }),
        ("Permissions", {
            "fields": (
                "role",
                "analytics_level",   # ← ADDED HERE
                "is_private",
                "is_blocked",
                "is_staff",
                "is_superuser",
                "is_active",
                "two_factor_enabled",
                "dark_mode",
            )
        }),
    )