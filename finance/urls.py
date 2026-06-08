from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.account_list,
        name='account_list'
    ),

    path(
        'add/',
        views.add_account,
        name='add_account'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_account,
        name='edit_account'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_account,
        name='delete_account'
    ),
]