from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, UserCreationForm
)
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.forms import (
    CharField, Form, Textarea,
    DecimalField, NumberInput, TextInput,
    ModelForm, ChoiceField, Select, ModelChoiceField,
    HiddenInput
)

from viewer.models.profile import Profile
from viewer.models.budget import Budget
from viewer.models.expence import Expence


class UpdateExpenseForm(ModelForm):
    class Meta:
        model = Expence
        fields = ["name", "value", "category"]

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


class CreateExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateExpenseForm, self).__init__(*args, **kwargs)
        self.budget = Budget.objects.filter(profile=self.request.user.profile)

    class Meta:
        model = Expence
        fields = ["name", "value", "category"]

        # widgets = {'budget': HiddenInput()}

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

    @atomic
    def save(self, commit=True):
        result = super().save(commit)
        name = self.cleaned_data["name"]
        value = self.cleaned_data["value"]
        category = self.cleaned_data["category"]
        budget = self.budget[0]
        expense = Expence(
            name=name,
            value=value,
            category=category,
            budget=budget

        )
        if commit:
            expense.save()
        return result


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ["username"]

    income = DecimalField(
        label="Your income: ",
        widget=NumberInput,
        max_digits=100000000,
        min_value=0,
        decimal_places=2
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)

        income = self.cleaned_data["income"]
        profile = Profile(income=income, user=result)
        budget = Budget(profile=profile, total_budget=income)
        if commit:
            profile.save()
            budget.save()
        return result


class UpdateBudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = "__all__"

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
