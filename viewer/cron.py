from datetime import datetime
from viewer.models.budget import Budget


def add_income_to_budget():
    queryset = Budget.objects.filter(profile__pay_day=datetime.now().day)
    for budget in queryset:
        budget.total_budget += budget.profile.income
        budget.save()
