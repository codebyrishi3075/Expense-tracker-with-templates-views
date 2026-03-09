from django.db import models
from django.conf import settings


class UserSettings(models.Model):

    DATE_FORMAT_CHOICES = [
        ('YYYY-MM-DD', 'YYYY-MM-DD'),
        ('DD-MM-YYYY', 'DD-MM-YYYY'),
    ]

    CURRENCY_CHOICES = [
        ('₹', 'INR (₹)'),
        ('$', 'USD ($)'),
        ('€', 'Euro (€)'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings'
    )

    currency = models.CharField(max_length=10, default='₹', choices=CURRENCY_CHOICES)

    monthly_budget = models.DecimalField(       # FIXED: was monthly_budget_limit
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    date_format = models.CharField(             # FIXED: field was missing
        max_length=20,
        default='YYYY-MM-DD',
        choices=DATE_FORMAT_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.email}"