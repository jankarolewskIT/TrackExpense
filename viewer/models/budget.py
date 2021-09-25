from django.db.models import Model, CharField, DecimalField, ForeignKey, DO_NOTHING

from viewer.models.expence import Expence

class Budget(Model):
    name = CharField(max_length=128)
    total_budget = DecimalField(max_digits=100000, decimal_places=2)
    netto_budget = DecimalField(max_digits=100000, decimal_places=2)
    tax = DecimalField(max_digits=100000, decimal_places=2)
    balance = DecimalField(max_digits=100000, decimal_places=2)
    expence = ForeignKey(Expence, on_delete=DO_NOTHING)

    def get_netto(self):
        pass

    def add_to_balance(self):
        pass
