from django.db.models import (
    Model, CharField, DecimalField,
    ForeignKey, CASCADE, OneToOneField,
    TextChoices, DateField, PositiveIntegerField,

)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    income = DecimalField(max_digits=1000000, decimal_places=2)
    # current_money = DecimalField(max_digits=1000000, decimal_places=2, null=True)
    pay_day = PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)], default=1)
    income_date = DateField(auto_now_add=True, null=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return self.user.get_full_name()
        return self.user.username

