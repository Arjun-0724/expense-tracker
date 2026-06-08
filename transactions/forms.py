from django import forms
from .models import Transaction,Category
from finance.models import Account


class TransactionForm(forms.ModelForm):

    def __init__(
        self,
        *args,
        user=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        if user:

            self.fields[
                'account'
            ].queryset = user.account_set.all()

            self.fields[
                'category'
            ].queryset = user.category_set.all()

    class Meta:
        model = Transaction

        fields = [
            'account',
            'category',
            'transaction_type',
            'amount',
            'description',
            'transaction_date',
        ]