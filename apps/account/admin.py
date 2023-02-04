from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import User, Account


# Register your models here.
@register(User)
class MainUserAdmin(UserAdmin):
    model = User

    list_display = (
        "account",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "username")
    ordering = ("first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "bio")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_contributor",
                    "is_editor",
                    "is_blog_owner",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super(MainUserAdmin, self).get_queryset(request)
        return qs.select_related()


@register(Account)
class MainAccountAdmin(ModelAdmin):
    model = Account

    list_display = (
        "created_date",
        "account_name",
        "contact_email"
    )
    list_filter = ("account_name", "contact_email")
    search_fields = ("account_name", "contact_email")
    ordering = ("-created_date", "account_name")

    def get_queryset(self, request):
        qs = super(MainAccountAdmin, self).get_queryset(request)
        return qs.select_related()