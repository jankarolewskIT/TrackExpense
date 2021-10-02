from django.db.models import Model, CharField, DecimalField, OneToOneField, CASCADE

from viewer.models.profile import Profile
from viewer.models.expence import Expence


class Budget(Model):
    profile = OneToOneField(Profile, on_delete=CASCADE, default=None)
    name = CharField(max_length=128, blank=True, null=True)
    total_budget = DecimalField(max_digits=100000, decimal_places=2, default=0)

    def add_to_balance(self, income):
        self.total_budget += income

    def budget_left(self):
        expenses = Expence.objects.filter(budget=self)
        total_expense = 0
        for expense in expenses:
            total_expense += expense.value
        return self.total_budget - total_expense

    def __str__(self):
        return f"{self.name} {self.total_budget}"
