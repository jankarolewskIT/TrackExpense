from django.db.models import (
    Model, CharField, DecimalField, DateField,
    OneToOneField, CASCADE, ForeignKey, TextChoices, DO_NOTHING
)

from viewer.models.budget import Budget


class Expence(Model):
    name = CharField(max_length=128)
    value = DecimalField(max_digits=10000, decimal_places=2)
    date = DateField(auto_now_add=True)
    budget = ForeignKey(Budget, on_delete=DO_NOTHING, null=True)

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
        default=Catagory.OTHER,
    )

    def __str__(self):
        return self.name
