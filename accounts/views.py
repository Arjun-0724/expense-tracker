from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transactions.models import Transaction
import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from budgets.models import Budget
from django.utils import timezone

@login_required
def home(request):

    income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income'
    ).aggregate(total=Sum('amount'))

    expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))

    total_income = income['total'] or 0
    total_expenses = expenses['total'] or 0

    balance = total_income - total_expenses

    recent_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-transaction_date')[:5]
    # 
    category_expenses = (
        Transaction.objects.filter(
            user=request.user,
            transaction_type='expense'
        )
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        )
    category_labels = [
    item['category__name']
    for item in category_expenses
    ]

    category_totals = [
        float(item['total'])
        for item in category_expenses
    ]
    # 
    monthly_expenses = (
    Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    )
    .annotate(month=TruncMonth('transaction_date'))
    .values('month')
    .annotate(total=Sum('amount'))
    .order_by('month')
    
    )
    month_labels = [
        item['month'].strftime('%b %Y')
        for item in monthly_expenses
    ]
    month_totals = [
        float(item['total'])
        for item in monthly_expenses
    ]
    #
    today = timezone.now()

    current_month = today.month
    current_year = today.year

    budget_alerts = [] 
    # 
    budgets = Budget.objects.filter(
    user=request.user,
    month=current_month,
    year=current_year
)

    for budget in budgets:

        spent = (
            Transaction.objects.filter(
                user=request.user,
                category=budget.category,
                transaction_type='expense',
                transaction_date__month=current_month,
                transaction_date__year=current_year
            )
            .aggregate(total=Sum('amount'))
            ['total']
            or 0
        )

        percentage = (
            spent / budget.amount * 100
            if budget.amount > 0
            else 0
        )

        if percentage >= 100:

            excess = spent - budget.amount

            budget_alerts.append({
                'type': 'danger',
                'message':
                    f'{budget.category} budget exceeded by ₹{excess}'
            })

        elif percentage >= 80:

            budget_alerts.append({
                'type': 'warning',
                'message':
                    f'{budget.category} budget is {percentage:.0f}% used'
            })
        # 
        
    context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance,
            'recent_transactions': recent_transactions,
            
            'category_labels': json.dumps(category_labels),
            'category_totals': json.dumps(category_totals),
            
            'month_labels': json.dumps(month_labels),
            'month_totals': json.dumps(month_totals),
            'budget_alerts': budget_alerts,
        }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )