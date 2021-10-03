from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "user_id", "income", "income_date", "pay_day"]
    list_per_page = 10
    list_filter = ["pay_day"]

    fieldsets = [
        (None, {"fields": ["income", "pay_day"]})
    ]


class BudgetAdmin(admin.ModelAdmin):

    @staticmethod
    def name_display(obj):
        if obj.name is not None:
            return obj.name
        return "Empty"

    @staticmethod
    def total_budget_display(obj):
        return f"{obj.total_budget} zł"

    ordering = ["id"]
    list_display = ["id", "name_display", "total_budget_display"]


class ExpenseAdmin(admin.ModelAdmin):
    @staticmethod
    def value_display(obj):
        return f"{obj.value} zł"

    # @staticmethod
    # def date_display(obj):
    #     return obj.date | "date: %Y %m %d"

    ordering = ["id"]
    list_display = ["id", "name", "value_display", "date", "category", "is_cycle", "expense_monthly_date"]
    list_per_page = 20

    search_fields = ["name"]
    list_filter = ["budget_id"]


