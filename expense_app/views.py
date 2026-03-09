from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from datetime import datetime

from .models import Expense


@login_required
def expenses_page(request):
    return render(request, "expenses/expenses.html")


@login_required
@require_http_methods(["POST"])
def create_expense(request):
    try:
        category_id = request.POST.get("category", "").strip()
        amount      = request.POST.get("amount", "").strip()
        date_str    = request.POST.get("date", "").strip()
        notes       = request.POST.get("notes", "").strip()

        if not amount:
            return JsonResponse({"success": False, "message": "Amount is required"}, status=400)
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "message": "Amount must be a positive number"}, status=400)

        if not date_str:
            return JsonResponse({"success": False, "message": "Date is required"}, status=400)
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid date format"}, status=400)

        if category_id:
            try:
                category_id = int(category_id)
            except (ValueError, TypeError):
                return JsonResponse({"success": False, "message": "Invalid category"}, status=400)

        expense = Expense.objects.create(
            user=request.user,
            category_id=category_id if category_id else None,
            amount=amount,
            date=date_str,
            notes=notes
        )

        return JsonResponse({"success": True, "message": "Expense created successfully", "id": expense.id})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
def list_expenses(request):
    try:
        qs = Expense.objects.filter(user=request.user)

        search = request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(Q(notes__icontains=search))

        category = request.GET.get("category", "").strip()
        if category:
            try:
                qs = qs.filter(category_id=int(category))
            except (ValueError, TypeError):
                pass

        from_date = request.GET.get("from", "").strip()
        to_date   = request.GET.get("to", "").strip()
        if from_date and to_date:
            qs = qs.filter(date__range=[from_date, to_date])

        paginator   = Paginator(qs.order_by('-date'), 10)
        page_number = request.GET.get("page", 1)
        page        = paginator.get_page(page_number)

        data = [
            {
                "id":          e.id,
                "category_id": e.category_id,
                "category":    e.category.name if e.category else "Uncategorized",
                "amount":      float(e.amount),
                "date":        str(e.date),
                "notes":       e.notes or ""
            }
            for e in page
        ]

        return JsonResponse({
            "count":        paginator.count,
            "num_pages":    paginator.num_pages,
            "current_page": page.number,
            "data":         data
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def update_expense(request, pk):
    try:
        expense = Expense.objects.filter(id=pk, user=request.user).first()
        if not expense:
            return JsonResponse({"success": False, "message": "Expense not found"}, status=404)

        category_id = request.POST.get("category", "").strip()
        amount      = request.POST.get("amount", "").strip()
        date_str    = request.POST.get("date", "").strip()
        notes       = request.POST.get("notes", "").strip()

        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError()
                expense.amount = amount
            except (ValueError, TypeError):
                return JsonResponse({"success": False, "message": "Amount must be a positive number"}, status=400)

        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                expense.date = date_str
            except ValueError:
                return JsonResponse({"success": False, "message": "Invalid date format"}, status=400)

        if category_id:
            try:
                expense.category_id = int(category_id)
            except (ValueError, TypeError):
                return JsonResponse({"success": False, "message": "Invalid category"}, status=400)

        # notes can be empty string (clearing it is valid)
        expense.notes = notes
        expense.save()

        return JsonResponse({"success": True, "message": "Expense updated successfully"})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def delete_expense(request, pk):
    try:
        expense = Expense.objects.filter(id=pk, user=request.user).first()
        if not expense:
            return JsonResponse({"success": False, "message": "Expense not found"}, status=404)
        expense.delete()
        return JsonResponse({"success": True, "message": "Expense deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)