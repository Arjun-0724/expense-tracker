from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Account, Category, Transaction

@login_required
def add_transaction(request):

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            transaction = form.save(
                commit=False
            )

            transaction.user = request.user

            transaction.save()

            return redirect('home')

    else:

        form = TransactionForm(
            user=request.user
        )

    return render(
        request,
        'transactions/add_transaction.html',
        {'form': form}
    )
    
    
@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-transaction_date')

    context = {
        'transactions': transactions
    }

    return render(
        request,
        'transactions/transaction_list.html',
        context
    )