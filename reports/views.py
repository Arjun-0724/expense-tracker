from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ReportFilterForm
from transactions.models import Transaction
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

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
@login_required
def export_excel(request):

    form = ReportFilterForm(request.GET)

    if not form.is_valid():
        return HttpResponse(
            "Invalid date range",
            status=400
        )

    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']

    transactions = (
        Transaction.objects.filter(
            user=request.user,
            transaction_date__range=(
                start_date,
                end_date
            )
        )
        .order_by('-transaction_date')
    )

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Transactions"

    worksheet.append([
        "Date",
        "Type",
        "Category",
        "Amount"
    ])

    for transaction in transactions:

        worksheet.append([
            str(transaction.transaction_date),
            transaction.transaction_type,
            str(transaction.category),
            float(transaction.amount)
        ])

    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="transactions_report.xlsx"'
    )

    workbook.save(response)

    return response

@login_required
def export_pdf(request):

    form = ReportFilterForm(request.GET)

    if not form.is_valid():

        return HttpResponse(
            "Invalid date range",
            status=400
        )

    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']

    transactions = (
        Transaction.objects.filter(
            user=request.user,
            transaction_date__range=(
                start_date,
                end_date
            )
        )
        .order_by('-transaction_date')
    )

    buffer = BytesIO()

    document = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Transaction Report",
            styles['Title']
        )
    )

    elements.append(
        Paragraph(
            f"Period: {start_date} to {end_date}",
            styles['Normal']
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    data = [
        [
            "Date",
            "Type",
            "Category",
            "Amount"
        ]
    ]

    total_income = 0
    total_expense = 0

    for transaction in transactions:

        data.append([
            str(transaction.transaction_date),
            transaction.transaction_type,
            str(transaction.category),
            str(transaction.amount)
        ])

        if transaction.transaction_type == "income":
            total_income += transaction.amount
        else:
            total_expense += transaction.amount

    table = Table(data)

    table.setStyle(
        TableStyle([
            (
                'BACKGROUND',
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                'GRID',
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            f"Total Income: ₹{total_income}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"Total Expense: ₹{total_expense}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"Net Balance: ₹{total_income - total_expense}",
            styles['Normal']
        )
    )

    document.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="transactions_report.pdf"'
    )

    return response