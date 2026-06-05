from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        'transactions.Category',
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        'transactions.Category',
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    month = models.IntegerField(
        default=timezone.now().month
    )

    year = models.IntegerField(
        default=timezone.now().year
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.category}"
            f" ({self.month}/{self.year})"
        )
class Meta:

    unique_together = (
        'user',
        'category',
        'month',
        'year'
    )