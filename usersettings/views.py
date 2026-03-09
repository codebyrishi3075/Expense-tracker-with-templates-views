from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import UserSettings


@login_required
def settings_page(request):
    return render(request, "usersettings/settings.html")


@login_required
def get_user_settings(request):
    try:
        obj, _ = UserSettings.objects.get_or_create(user=request.user)
        return JsonResponse({
            "success": True,
            "data": {
                "currency":    obj.currency,
                "date_format": obj.date_format,
            }
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def update_user_settings(request):
    try:
        obj, _ = UserSettings.objects.get_or_create(user=request.user)
        currency    = request.POST.get("currency", "").strip()
        date_format = request.POST.get("date_format", "").strip()
        if currency:
            obj.currency = currency
        if date_format:
            obj.date_format = date_format
        obj.save()
        return JsonResponse({
            "success": True,
            "message": "Settings updated successfully",
            "data": {"currency": obj.currency, "date_format": obj.date_format}
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)