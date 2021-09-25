from django.db.models import Model, CharField, DecimalField, DateField, OneToOneField, CASCADE

from viewer.models.category import Category


class Expence(Model):
    name = CharField(max_length=128)
    value = DecimalField(max_digits=10000, decimal_places=2)
    date = DateField(auto_now_add=True)
    category = OneToOneField(Category, on_delete=CASCADE)
