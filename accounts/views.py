from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transactions.models import Transaction

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

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
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