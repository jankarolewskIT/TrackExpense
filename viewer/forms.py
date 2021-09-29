from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, UserCreationForm
)
from django.db.transaction import atomic
from django.forms import (
    CharField, Form, Textarea,
    DecimalField, NumberInput, TextInput,
    ModelForm
)

from viewer.models.profile import Profile
from viewer.models.budget import Budget


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
        widget=TextInput,
    )

    total_budget = DecimalField(
        label="Enter your budget: ",
        min_value=0,
        max_digits=10000000,
        decimal_places=2,
        widget=NumberInput,
    )





