from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'date', 'created_at']
    list_filter = ['date', 'category', 'user', 'created_at']
    search_fields = ['notes', 'user__email', 'category__name']
    readonly_fields = ['created_at']
    ordering = ['-date']
    date_hierarchy = 'date'

    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Expense Details', {'fields': ('category', 'amount', 'date', 'notes')}),
        ('Metadata', {'fields': ('created_at',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs
