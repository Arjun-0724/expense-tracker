from django import forms
from finance.models import Account


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account

        fields = [
            'name',
            'account_type',
            'opening_balance'
        ]