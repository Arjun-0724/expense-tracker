from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ReportFilterForm
from transactions.models import Transaction

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