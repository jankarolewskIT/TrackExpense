from datetime import datetime
from viewer.models.budget import Budget, Expence


# def add_income_to_budget():
#     queryset = Budget.objects.filter(profile__pay_day=datetime.now().day)
#     for budget in queryset:
#         budget.total_budget = budget.current_budget()
#         Expence.objects.filter(budget=budget).delete()
#         budget.total_budget += budget.profile.income
#         budget.save()
#
#
# def cycle_expense():
#     queryset = Expence.objects.filter(is_cycle=True).filter(expense_monthly_date=datetime.now().day)
#     for expense in queryset:
#         Expence.objects.create(
#             name=expense.name,
#             category=expense.category,
#             budget=expense.budget,
#             value=expense.value,
#             is_cycle=expense.is_cycle,
#             expense_monthly_date=expense.expense_monthly_date
#         )
#         expense.delete()
