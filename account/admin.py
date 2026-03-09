from django.contrib import admin
from .models import User, EmailOTP


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_email_verified', 'is_active', 'date_joined']
    list_filter = ['is_email_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'username']
    readonly_fields = ['date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Email', {'fields': ('is_email_verified',)}),
        ('Dates', {'fields': ('date_joined', 'last_login')}),
    )


class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'purpose', 'is_used', 'created_at', 'is_expired']
    list_filter = ['purpose', 'is_used', 'created_at']
    search_fields = ['user__email', 'otp']
    readonly_fields = ['created_at', 'otp']


admin.site.register(User, UserAdmin)
admin.site.register(EmailOTP, EmailOTPAdmin)
