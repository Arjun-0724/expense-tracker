from django.shortcuts import render

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