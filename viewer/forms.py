from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm
)
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import (
    CharField, DecimalField, NumberInput,
    TextInput, ModelForm, ChoiceField,
    Select, IntegerField, BooleanField,
    CheckboxInput, Form

)

from viewer.models.budget import Budget, Expence
from viewer.models.profile import Profile


# =====================================================================
# Expense Forms
# =======================================================================

class CreateExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateExpenseForm, self).__init__(*args, **kwargs)
        self.budget = Budget.objects.filter(profile=self.request.user.profile)

    class Meta:
        model = Expence
        fields = [
            "name", "value", "category",
            "is_cycle", "expense_monthly_date"
        ]

    name = CharField(
        label="Expense name: ",
        max_length=128,
        widget=TextInput
    )

    value = DecimalField(
        label="Amount: ",
        max_digits=100000000,
        widget=NumberInput,
        decimal_places=2,
        min_value=0.01
    )

    category = ChoiceField(
        choices=Expence.Catagory.choices,
        label="Category: ",
        widget=Select
    )

    is_cycle = BooleanField(
        label="Is cycle?",
        initial=False,
        widget=CheckboxInput,
        required=False
    )

    expense_monthly_date = IntegerField(
        label="Day od cycle",
        min_value=1,
        max_value=31,
        widget=NumberInput,
        required=False

    )

    def clean_value(self):
        data = self.cleaned_data["value"]
        if data > self.request.user.profile.budget.current_budget():
            raise ValidationError("Budget not enough")
        return data

    def save(self, commit=True):
        name = self.cleaned_data["name"]
        value = self.cleaned_data["value"]
        category = self.cleaned_data["category"]
        is_cycle = self.cleaned_data["is_cycle"]
        expense_monthly_date = self.cleaned_data["expense_monthly_date"]

        budget = self.budget[0]

        expense = Expence(
            name=name,
            value=value,
            category=category,
            budget=budget,
            is_cycle=is_cycle,
            expense_monthly_date=expense_monthly_date

        )
        if commit:
            expense.save()
            budget.current_budget()
            budget.save()
        return expense


class UpdateExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UpdateExpenseForm, self).__init__(*args, **kwargs)
        self.budget = Budget.objects.filter(profile=self.request.user.profile)

    class Meta:
        model = Expence
        fields = ["name", "value", "category", "is_cycle", "expense_monthly_date"]

    name = CharField(
        label="Expense name: ",
        max_length=128,
        widget=TextInput
    )

    value = DecimalField(
        label="Amount: ",
        validators=[],
        max_digits=100000000,
        decimal_places=2,
        min_value=0.01
    )

    category = ChoiceField(
        choices=Expence.Catagory.choices,
        label="Category: ",
        widget=Select
    )
    is_cycle = BooleanField(
        label="Is cycle?",
        initial=False,
        required=False,
        widget=CheckboxInput
    )

    expense_monthly_date = IntegerField(
        label="Day od cycle",
        min_value=1,
        max_value=31,
        required=False,
        widget=NumberInput

    )

    # def save(self, commit=True):
    #     budget = self.request.user.profile.budget
    #     budget.total_budget = float(budget.total_budget)
    #     budget.total_budget += self.request.
    #     if commit:
    #         budget.save()
    #     return budget


# =====================================================================
# Profile Forms
# =======================================================================

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ["username"]

    current_money = DecimalField(
        label="Your current budget: ",
        widget=NumberInput,
        max_digits=100000000,
        min_value=0,
        decimal_places=2
    )

    income = DecimalField(
        label="Your income: ",
        widget=NumberInput,
        max_digits=100000000,
        min_value=0,
        decimal_places=2
    )

    pay_day = IntegerField(
        label="Your salary day",
        min_value=1,
        max_value=31,

    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)

        current_money = self.cleaned_data["current_money"]
        income = self.cleaned_data["income"]
        pay_day = self.cleaned_data["pay_day"]
        profile = Profile(income=income, user=result, pay_day=pay_day)
        budget = Budget(profile=profile, total_budget=current_money)
        initial_permissions = [
            Permission.objects.get(codename="add_expence"),
            Permission.objects.get(codename="change_expence"),
            Permission.objects.get(codename="delete_expence"),
            Permission.objects.get(codename="view_expence"),
            Permission.objects.get(codename="change_budget"),
            Permission.objects.get(codename="change_profile"),
            Permission.objects.get(codename="delete_profile"),
        ]
        if commit:
            for permission in initial_permissions:
                result.user_permissions.add(permission)
            profile.save()
            budget.save()
        return result


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["pay_day", "income"]

    income = DecimalField(
        label="Enter Your income",
        decimal_places=2,
        max_digits=100000000,
        widget=NumberInput

    )

    pay_day = DecimalField(
        label="Income date",
        widget=NumberInput,
        max_digits=2,
        decimal_places=0
    )


class FormPasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form.control"


# =====================================================================
# Budget Forms
# =======================================================================


class UpdateBudgetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form.control"

    class Meta:
        model = Budget
        fields = ["name", "total_budget"]

    name = CharField(
        label="Enter your budget name: ",
        min_length=2,
        required=False,
        widget=TextInput
    )

    total_budget = DecimalField(
        label="Enter your budget: ",
        min_value=0,
        required=False,
        max_digits=10000000,
        decimal_places=2,
        widget=NumberInput
    )


class UpdateTotalBudgetForm(Form):
    class Meta:
        model = Budget
        fields = ["income"]

    income = DecimalField(
        label="Add",
        widget=NumberInput,
        decimal_places=2,
        max_digits=10000000
    )
