from django.urls import path
from . import views

urlpatterns = [
    path(
        'add/',
        views.add_transaction,
        name='add_transaction'
    ),
    path(
        '',
        views.transaction_list,
        name='transaction_list'
    ),
]