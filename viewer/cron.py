from datetime import datetime
from viewer.models.budget import Budget, Expence


def add_income_to_budget():
    queryset = Budget.objects.filter(profile__pay_day=datetime.now().day)
    for budget in queryset:
        budget.total_budget = budget.current_budget()
        budget.total_budget += budget.profile.income
        budget.save()
    expenses = Expence.objects.filter(budget__profile__pay_day=datetime.now().day). \
        filter(is_archive=False).filter(is_cycle=False)
    for invalid_expense in expenses:
        invalid_expense.is_archive = True
        invalid_expense.save()


def cycle_expense():
    queryset = Expence.objects.filter(is_cycle=True). \
        filter(expense_monthly_date=datetime.now().day). \
        filter(is_archive=False)
    for expense in queryset:
        expense.is_archive = True
        expense.save()
        Expence.objects.create(
            name=expense.name,
            category=expense.category,
            budget=expense.budget,
            value=expense.value,
            is_cycle=expense.is_cycle,
            expense_monthly_date=expense.expense_monthly_date
        )
