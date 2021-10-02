from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, UserCreationForm
)
from django.db.transaction import atomic
from django.forms import (
    CharField, DecimalField, NumberInput,
    TextInput, ModelForm, ChoiceField,
    Select, DateField, IntegerField, BooleanField,
    CheckboxInput, SelectDateWidget, RadioSelect

)

from viewer.models.profile import Profile
from viewer.models.budget import Budget
from viewer.models.expence import Expence


class UpdateExpenseForm(ModelForm):
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
            widget=CheckboxInput
        )

        expense_monthly_date = IntegerField(
            label="Day od cycle",
            min_value=1,
            max_value=31,
            widget=NumberInput

        )


class CreateExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateExpenseForm, self).__init__(*args, **kwargs)
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
        widget=CheckboxInput
    )

    expense_monthly_date = IntegerField(
        label="Day od cycle",
        min_value=1,
        max_value=31,
        widget=NumberInput

    )

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
        return expense


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

    # income_date = DateField(
    #     label=""
    # )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)

        current_money = self.cleaned_data["current_money"]
        income = self.cleaned_data["income"]
        pay_day = self.cleaned_data["pay_day"]
        profile = Profile(income=income, user=result, pay_day=pay_day)
        budget = Budget(profile=profile, total_budget=current_money)
        if commit:
            profile.save()
            budget.save()
        return result


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["income"]

    income = DecimalField(
        label="Enter Your income",
        decimal_places=2,
        max_digits=100000000,
        widget=NumberInput

    )


class UpdateBudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ["name", "total_budget"]

    name = CharField(
        label="Enter your budget name: ",
        min_length=2,
        widget=TextInput
    )

    total_budget = DecimalField(
        label="Enter your budget: ",
        min_value=0,
        max_digits=10000000,
        decimal_places=2,
        widget=NumberInput
    )
