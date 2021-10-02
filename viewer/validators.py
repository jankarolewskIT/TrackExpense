# from django.forms import NumberInput, IntegerField
# from django.core.exceptions import ValidationError
#
#
# class BudgetGraterExpense(object):
#     def __init__(self, request):
#         self.request = request
#
#     def __call__(self, *args, **kwargs):
#         pass
#
#     def validate(self, value):
#         if value > self.request.user.profile.budget.total_budget:
#             raise ValidationError("Not enought money in your budget")


