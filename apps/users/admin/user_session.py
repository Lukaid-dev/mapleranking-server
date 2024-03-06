from django.contrib import admin
from apps.users.models import UserSession


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "user",
                    "issued_at",
                    "accessed_at",
                    "logged_out_at",
                    "expired_at",
                    "is_expired",
                    "social",
                    "count",
                ),
            },
        ),
    )
    readonly_fields = (
        "user",
        "issued_at",
        "accessed_at",
        "logged_out_at",
        "expired_at",
        "is_expired",
        "social",
        "count",
    )
    list_display = (
        "id",
        "user",
        "accessed_at",
        "logged_out_at",
        "is_expired",
        "count",
    )
    list_display_links = (
        "id",
        "user",
    )
