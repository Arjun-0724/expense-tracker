from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import  Category, Transaction
from finance.models import Account

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
    

@login_required
def edit_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            instance=transaction,
            user=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                'transaction_list'
            )

    else:

        form = TransactionForm(
            instance=transaction,
            user=request.user
        )

    return render(
        request,
        'transactions/edit_transaction.html',
        {'form': form}
    )    
    
@login_required
def delete_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    if request.method == "POST":

        transaction.delete()

        return redirect(
            'transaction_list'
        )

    return render(
        request,
        'transactions/delete_transaction.html',
        {'transaction': transaction}
    )