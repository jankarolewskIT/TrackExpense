from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, UserCreationForm
)
from django.db.transaction import atomic
from django.forms import CharField, Form, Textarea, DecimalField, NumberInput

from viewer.models.profile import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ["username", "first_name"]

    income = DecimalField(
        label="Your income: ",
        widget=NumberInput,
        max_digits=100000000,
        min_value=0,
        decimal_places=2
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = False
        result = super().save(commit)

        income = self.cleaned_data["income"]
        profile = Profile(income=income, user=result)
        if commit:
            profile.save()
        return result
