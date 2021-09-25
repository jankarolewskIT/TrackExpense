from django.db.models import Model, DecimalField, TextChoices, CharField


class Category(Model):
    class Types(TextChoices):
        TRANSPORT = "TR", "Transport"
        ENTERTAINMENT = "ET", "Entertainment"
        HEALTH = "PH", "Health"
        CLOTHES = "CT", "Clothes"
        FOOD = "FD", "Food"
        ACCOMMODATION = "AD", "Accommodation"
        OTHER = "OT", "Others"

    category = CharField(
        max_length=2,
        choices=Types.choices,
        default=Types.OTHER,
    )

    sum_value = DecimalField(max_digits=1000000, decimal_places=2)
