from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget

        fields = [
            'category',
            'amount'
        ]

    def __init__(
        self,
        *args,
        user=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            'category'
        ].queryset = (
            self.fields[
                'category'
            ].queryset.filter(
                user=user
            )
        )
        
fields = [
    'category',
    'amount',
    'month',
    'year'
]