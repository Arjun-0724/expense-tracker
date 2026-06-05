from django.shortcuts import render
from django.db.models import Sum
from transactions.models import Transaction
from .models import Budget
from budgets.models import Budget
from django.utils import timezone
# Create your views here.
from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth.decorators import (
    login_required
)

from .forms import BudgetForm


@login_required
def add_budget(request):

    if request.method == "POST":

        form = BudgetForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            budget = form.save(
                commit=False
            )

            budget.user = request.user

            budget.save()

            return redirect(
                'budget_list'
            )

    else:

        form = BudgetForm(
            user=request.user
        )

    return render(
        request,
        'budgets/add_budget.html',
        {'form': form}
    )
    
@login_required
def budget_list(request):

    budgets = Budget.objects.filter(
        user=request.user
    )

    budget_data = []

    for budget in budgets:
        spent = (
    Transaction.objects.filter(
        user=request.user,
        category=budget.category,
        transaction_type='expense',
        transaction_date__month=budget.month,
        transaction_date__year=budget.year
    )
    .aggregate(
        total=Sum('amount')
    )['total']
    or 0
)

        remaining = budget.amount - spent

        percentage = (
            spent / budget.amount * 100
            if budget.amount > 0
            else 0
        )

        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percentage': min(
                percentage,
                100
            ),
            'exceeded': spent > budget.amount
        })

    return render(
        request,
        'budgets/budget_list.html',
        {
            'budget_data': budget_data
        }
    )