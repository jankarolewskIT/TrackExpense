from django.db.models import Model, CharField, DecimalField, ForeignKey, CASCADE, OneToOneField, TextChoices
from django.contrib.auth.models import User


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    income = DecimalField(max_digits=1000000, decimal_places=2)

