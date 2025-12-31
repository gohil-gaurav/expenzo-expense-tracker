from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    TRANSATION_TYPE = (
        ('INCOME', 'income'),
        ('EXPENSE', 'expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSATION_TYPE)

    def __str__(self):
        return f"{self.title} - {self.amount}"

