from datetime import date, datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from expense_app.models import Expense
from budget_app.models import Budget
from usersettings.models import UserSettings


@login_required
def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")


@login_required
def dashboard_summary(request):
    try:
        user = request.user

        # ── DATE FILTER ──────────────────────────────────────
        month_param = request.GET.get('month', '').strip()

        if month_param:
            try:
                year, month = map(int, month_param.split('-'))
                start_date  = date(year, month, 1)
                if month == 12:
                    end_date = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_date = date(year, month + 1, 1) - timedelta(days=1)
            except (ValueError, IndexError):
                today      = date.today()
                start_date = date(today.year, today.month, 1)
                end_date   = today
        else:
            today      = date.today()
            start_date = date(today.year, today.month, 1)
            end_date   = today

        budget_month = date(start_date.year, start_date.month, 1)

        # ── CURRENCY ─────────────────────────────────────────
        settings_obj, _ = UserSettings.objects.get_or_create(user=user)
        currency = settings_obj.currency or '₹'

        # ── EXPENSES grouped by category ─────────────────────
        expense_qs = (
            Expense.objects
            .filter(user=user, date__range=[start_date, end_date])
            .values('category_id', 'category__name')
            .annotate(spent=Sum('amount'))
        )

        expense_map = {}   # category_id -> {name, spent}
        for row in expense_qs:
            expense_map[row['category_id']] = {
                'name':  row['category__name'] or 'Uncategorized',
                'spent': float(row['spent']),
            }

        total_expense = sum(v['spent'] for v in expense_map.values())

        # ── BUDGETS for that month ────────────────────────────
        budget_qs = (
            Budget.objects
            .filter(user=user, month=budget_month)
            .select_related('category')
        )

        budget_map = {b.category_id: float(b.amount) for b in budget_qs}

        # ── BUILD CATEGORY ROWS ───────────────────────────────
        categories = []
        all_cat_ids = set(list(expense_map.keys()) + list(budget_map.keys()))

        remaining_budget = 0.0

        for cat_id in all_cat_ids:
            info      = expense_map.get(cat_id, {'name': None, 'spent': 0.0})
            spent     = info['spent']
            budget_amt = budget_map.get(cat_id, 0.0)

            # get category name from budget queryset if not in expense
            if info['name'] is None:
                b = next((b for b in budget_qs if b.category_id == cat_id), None)
                name = b.category.name if b else 'Uncategorized'
            else:
                name = info['name']

            remaining        = budget_amt - spent
            remaining_budget += max(remaining, 0)

            categories.append({
                'category':  name,
                'spent':     round(spent, 2),
                'budget':    round(budget_amt, 2),
                'remaining': round(remaining, 2),
                'exceeded':  spent > budget_amt if budget_amt > 0 else False,
            })

        # Sort by most spent first
        categories.sort(key=lambda x: x['spent'], reverse=True)

        return JsonResponse({
            'success':          True,
            'currency':         currency,
            'from':             str(start_date),
            'to':               str(end_date),
            'total_expense':    round(total_expense, 2),
            'remaining_budget': round(remaining_budget, 2),
            'categories':       categories,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': str(e)}, status=500)