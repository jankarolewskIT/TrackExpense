from datetime import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    Model, CharField, DecimalField, OneToOneField, CASCADE, DateField, ForeignKey, BooleanField,
    IntegerField, TextChoices, FloatField, DateTimeField
)
from viewer.models.profile import Profile


class Budget(Model):
    profile = OneToOneField(Profile, on_delete=CASCADE, default=None)
    name = CharField(max_length=128, blank=True, null=True)
    total_budget = DecimalField(max_digits=100000, decimal_places=2, default=0)

    def current_budget(self):
        queryset = Expence.objects.filter(budget=self).filter(is_archive=False)
        total_expenses = 0
        for expense in queryset:
            total_expenses += expense.value
        # total_expenses = float(total_expenses)
        return round(Decimal(self.total_budget) - Decimal(total_expenses), 2)

    def __str__(self):
        return f"{self.name} {self.total_budget}"


class Expence(Model):
    name = CharField(max_length=128)
    value = DecimalField(max_digits=10000, decimal_places=2)
    date = DateTimeField(auto_now_add=True, null=True)
    budget = ForeignKey(Budget, on_delete=CASCADE, null=True)
    is_archive = BooleanField(default=False, null=True, blank=True)
    is_cycle = BooleanField(default=False)
    expense_monthly_date = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)], null=True, blank=True)

    class Catagory(TextChoices):
        TRANSPORT = "TR", "Transport"
        ENTERTAINMENT = "ET", "Entertainment"
        HEALTH = "PH", "Health"
        CLOTHES = "CT", "Clothes"
        FOOD = "FD", "Food"
        ACCOMMODATION = "AD", "Accommodation"
        OTHER = "OT", "Others"

    category = CharField(
        max_length=2,
        choices=Catagory.choices,
        default=Catagory.OTHER
    )

    def __str__(self):
        return f"{self.name} ({self.value})"
