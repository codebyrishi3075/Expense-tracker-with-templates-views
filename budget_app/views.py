


from datetime import date
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.http import require_http_methods

from .models import BudgetCategory, Budget
from expense_app.models import Expense


@login_required
def categories_page(request):
    return render(request, "budget/categories.html")


@login_required
@require_http_methods(["POST"])
def create_category(request):
    try:
        name = request.POST.get("name", "").strip()
        if not name:
            return JsonResponse({"success": False, "message": "Category name is required"}, status=400)
        if len(name) > 100:
            return JsonResponse({"success": False, "message": "Name must be under 100 characters"}, status=400)
        if BudgetCategory.objects.filter(user=request.user, name=name).exists():
            return JsonResponse({"success": False, "message": "Category already exists"}, status=400)

        cat = BudgetCategory.objects.create(user=request.user, name=name)
        return JsonResponse({"success": True, "message": "Category created", "id": cat.id, "name": cat.name})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
def list_categories(request):
    try:
        cats = BudgetCategory.objects.filter(user=request.user).order_by('name')
        return JsonResponse({"data": [{"id": c.id, "name": c.name} for c in cats]})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def delete_category(request, pk):
    try:
        cat = BudgetCategory.objects.filter(id=pk, user=request.user).first()
        if not cat:
            return JsonResponse({"success": False, "message": "Category not found"}, status=404)
        cat.delete()
        return JsonResponse({"success": True, "message": "Category deleted"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
def budget_page(request):
    return render(request, "budget/budget.html")


@login_required
@require_http_methods(["POST"])
def create_budget(request):
    try:
        category_id = request.POST.get("category", "").strip()
        amount      = request.POST.get("amount", "").strip()
        month_raw   = request.POST.get("month", "").strip()

        if not category_id:
            return JsonResponse({"success": False, "message": "Category is required"}, status=400)
        if not amount:
            return JsonResponse({"success": False, "message": "Amount is required"}, status=400)
        if not month_raw:
            return JsonResponse({"success": False, "message": "Month is required"}, status=400)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "message": "Amount must be a positive number"}, status=400)

        try:
            year, month = month_raw.split("-")
            month_start = date(int(year), int(month), 1)
        except (ValueError, IndexError):
            return JsonResponse({"success": False, "message": "Invalid month format"}, status=400)

        try:
            category = BudgetCategory.objects.get(id=int(category_id), user=request.user)
        except BudgetCategory.DoesNotExist:
            return JsonResponse({"success": False, "message": "Category not found"}, status=404)

        if Budget.objects.filter(user=request.user, category=category, month=month_start).exists():
            return JsonResponse({"success": False, "message": "Budget for this category and month already exists"}, status=400)

        budget = Budget.objects.create(
            user=request.user, category=category, amount=amount, month=month_start
        )
        return JsonResponse({"success": True, "message": "Budget created", "id": budget.id})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
def list_budgets(request):
    try:
        budgets = Budget.objects.filter(user=request.user).select_related("category").order_by('-month')
        return JsonResponse({
            "data": [
                {
                    "id":          b.id,
                    "category_id": b.category_id,
                    "category":    b.category.name,
                    "amount":      float(b.amount),
                    "month":       str(b.month)
                }
                for b in budgets
            ]
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def edit_budget(request, pk):
    try:
        budget = Budget.objects.filter(id=pk, user=request.user).select_related('category').first()
        if not budget:
            return JsonResponse({"success": False, "message": "Budget not found"}, status=404)

        category_id = request.POST.get("category", "").strip()
        amount      = request.POST.get("amount", "").strip()
        month_raw   = request.POST.get("month", "").strip()

        if category_id:
            try:
                cat = BudgetCategory.objects.get(id=int(category_id), user=request.user)
                budget.category = cat
            except BudgetCategory.DoesNotExist:
                return JsonResponse({"success": False, "message": "Category not found"}, status=404)

        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError()
                budget.amount = amount
            except (ValueError, TypeError):
                return JsonResponse({"success": False, "message": "Amount must be a positive number"}, status=400)

        if month_raw:
            try:
                year, month = month_raw.split("-")
                budget.month = date(int(year), int(month), 1)
            except (ValueError, IndexError):
                return JsonResponse({"success": False, "message": "Invalid month format"}, status=400)

        budget.save()
        return JsonResponse({"success": True, "message": "Budget updated successfully", "id": budget.id})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def delete_budget(request, pk):
    try:
        budget = Budget.objects.filter(id=pk, user=request.user).first()
        if not budget:
            return JsonResponse({"success": False, "message": "Budget not found"}, status=404)
        budget.delete()
        return JsonResponse({"success": True, "message": "Budget deleted"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
def budget_utilization(request):
    try:
        today       = date.today()
        month_start = date(today.year, today.month, 1)
        budgets     = Budget.objects.filter(user=request.user, month=month_start).select_related("category")
        data = []
        for b in budgets:
            spent = Expense.objects.filter(
                user=request.user, category=b.category, date__gte=month_start
            ).aggregate(total=Sum("amount"))["total"] or 0
            remaining = float(b.amount) - float(spent)
            data.append({
                "category":  b.category.name,
                "budget":    float(b.amount),
                "spent":     float(spent),
                "remaining": remaining
            })
        return JsonResponse({"data": data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)