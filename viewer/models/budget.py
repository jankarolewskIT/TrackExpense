from django.db.models import Model, CharField, DecimalField, ForeignKey, DO_NOTHING, OneToOneField, CASCADE

from viewer.models.profile import Profile


class Budget(Model):
    profile = OneToOneField(Profile, on_delete=CASCADE, default=None)
    name = CharField(max_length=128, blank=True, null=True)
    total_budget = DecimalField(max_digits=100000, decimal_places=2, default=0)

    def add_to_balance(self, income):
        self.total_budget += income

    def __str__(self):
        if self.profile.user.first_name:
            user = self.profile.user.first_name
        else:
            user = self.profile.user.username

        return f"{user}'s {self.name}"
