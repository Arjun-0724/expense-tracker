from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.report_view,
        name='report_view'
    ),
    path(
        'export_csv/',
        views.export_csv,
        name='export_csv'
    ),
    path(
        'export_excel/',
        views.export_excel,
        name='export_excel'
    ),
    path(
    'export/pdf/',
    views.export_pdf,
    name='export_pdf'
),
]
