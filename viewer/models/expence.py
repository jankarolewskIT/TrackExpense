from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    Model, CharField, DecimalField, DateField,
    CASCADE, ForeignKey, TextChoices,
    BooleanField, IntegerField
)

from viewer.models.budget import Budget


class Expence(Model):
    name = CharField(max_length=128)
    value = DecimalField(max_digits=10000, decimal_places=2)
    date = DateField(auto_now_add=True)
    budget = ForeignKey(Budget, on_delete=CASCADE, null=True)
    is_cycle = BooleanField(default=False)
    expense_monthly_date = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)], null=True)

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
