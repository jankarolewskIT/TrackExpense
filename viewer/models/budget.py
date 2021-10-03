from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    Model, CharField, DecimalField, OneToOneField, CASCADE, DateField, ForeignKey, BooleanField,
    IntegerField, TextChoices
)
from viewer.models.profile import Profile


# import profile


class Budget(Model):
    profile = OneToOneField(Profile, on_delete=CASCADE, default=None)
    name = CharField(max_length=128, blank=True, null=True)
    total_budget = DecimalField(max_digits=100000, decimal_places=2, default=0)

    def add_to_budget(self, income):
        self.total_budget += income

    def __str__(self):
        return f"{self.name} {self.total_budget}"


class Expence(Model):
    name = CharField(max_length=128)
    value = DecimalField(max_digits=10000, decimal_places=2)
    date = DateField(auto_now_add=True)
    budget = ForeignKey(Budget, on_delete=CASCADE, null=True)
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
