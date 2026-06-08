from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ReportFilterForm
from transactions.models import Transaction
import csv
from django.http import HttpResponse

@login_required
def report_view(request):

    form = ReportFilterForm()

    transactions = None

    if request.GET:

        form = ReportFilterForm(
            request.GET
        )

        if form.is_valid():

            start_date = form.cleaned_data[
                'start_date'
            ]

            end_date = form.cleaned_data[
                'end_date'
            ]

            transactions = (
                Transaction.objects.filter(
                    user=request.user,
                    transaction_date__range=(
                        start_date,
                        end_date
                    )
                )
                .order_by(
                    '-transaction_date'
                )
            )

    return render(
        request,
        'reports/report.html',
        {
            'form': form,
            'transactions': transactions
        }
    )
    
@login_required
def export_csv(request):

    form = ReportFilterForm(request.GET)

    if not form.is_valid():
        return HttpResponse(
            "Invalid date range",
            status=400
        )

    start_date = form.cleaned_data[
        'start_date'
    ]

    end_date = form.cleaned_data[
        'end_date'
    ]

    transactions = (
        Transaction.objects.filter(
            user=request.user,
            transaction_date__range=(
                start_date,
                end_date
            )
        )
        .order_by(
            '-transaction_date'
        )
    )

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="transactions_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Date',
        'Type',
        'Category',
        'Amount'
    ])

    for transaction in transactions:

        writer.writerow([
            transaction.transaction_date,
            transaction.transaction_type,
            transaction.category,
            transaction.amount,
        ])

    return response