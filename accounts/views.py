from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transactions.models import Transaction
import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth

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
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
        
        'category_labels': json.dumps(category_labels),
        'category_totals': json.dumps(category_totals),
        
        'month_labels': json.dumps(month_labels),
    'month_totals': json.dumps(month_totals),
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