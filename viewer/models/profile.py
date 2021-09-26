from django.db.models import Model, CharField, DecimalField, ForeignKey, CASCADE, OneToOneField, TextChoices
from django.contrib.auth.models import User


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    income = DecimalField(max_digits=1000000, decimal_places=2)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return self.user.get_full_name()
        return self.user.username

