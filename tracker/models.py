from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User  # Import the User model

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    remarks = models.TextField(null=True, blank=True)  # New field for remarks
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # New field for 'added_by'

    def __str__(self):
        return f"{self.type} - {self.amount}"

