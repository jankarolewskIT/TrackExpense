from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from viewer.models.budget import Budget, Expence
from viewer.models.profile import Profile
from viewer.forms import SignUpForm, CreateExpenseForm, UpdateExpenseForm, UpdateBudgetForm, UpdateProfileForm, \
    UpdateTotalBudgetForm


class ExpenseCreateView(PermissionRequiredMixin, CreateView):
    model = Expence
    form_class = CreateExpenseForm
    template_name = "add_edit_expense.html"
    success_url = reverse_lazy("home")
    permission_required = "viewer.add_expence"

    def get_form_kwargs(self):
        kwargs = super(ExpenseCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_invalid(self, form):
        return render(
            self.request, template_name="add_edit_expense.html",
            context={
                "form": form
            }
        )


class ExpenseEditView(PermissionRequiredMixin, UpdateView):
    model = Expence
    template_name = "add_edit_expense.html"
    form_class = UpdateExpenseForm
    success_url = reverse_lazy("home")
    permission_required = "viewer.change_expence"


class ExpenseDeleteView(PermissionRequiredMixin, DeleteView):
    model = Expence
    success_url = reverse_lazy("home")
    template_name = "delete_expense.html"
    permission_required = "viewer.view_expence"

    def get_object(self, queryset=None):
        return Expence.objects.get(id=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        self.request.user.profile.budget.total_budget = self.request.user.profile.budget.total_budget + self.get_object().value
        self.request.user.profile.budget.save()
        return super().post(request=request)


class ExpenseStatView(View):
    def get(self, request):
        expences = Expence.objects.filter(budget=self.request.user.profile.budget)
        transport_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="TR")
        entertainment_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="ET")
        health_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="PH")
        clothes_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="CT")
        food_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="FD")
        accommodation_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="AD")
        other_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="OT")

        sum_all_expences = sum(map(lambda x: x.value, expences))
        sum_transport = sum(map(lambda x: x.value, transport_query))
        sum_entertainment = sum(map(lambda x: x.value, entertainment_query))
        sum_health = sum(map(lambda x: x.value, health_query))
        sum_clothes = sum(map(lambda x: x.value, clothes_query))
        sum_food = sum(map(lambda x: x.value, food_query))
        sum_accommodation = sum(map(lambda x: x.value, accommodation_query))
        sum_other = sum(map(lambda x: x.value, other_query))

        saves = self.request.user.profile.budget.total_budget - sum_all_expences

        return render(
            request, template_name="profile_stat.html",
            context={
                "sum_transport": sum_transport,
                "saves": saves,
                "sum_entertainment": sum_entertainment,
                "sum_health": sum_health,
                "sum_clothes": sum_clothes,
                "sum_food": sum_food,
                "sum_accommodation": sum_accommodation,
                "sum_other": sum_other
            }
        )


class ProfileView(LoginRequiredMixin, View):
    model = Expence

    def get(self, request):
        categories = [category[1] for category in Expence.Catagory.choices]
        budget = self.request.user.profile.budget
        queryset = Expence.objects.filter(budget=budget)
        form = CreateExpenseForm
        add_to_budget_form = UpdateTotalBudgetForm

        return render(
            request, template_name="profile.html",
            context={
                "expenses": queryset,
                "budget": budget,
                "categories": categories,
                "form": form,
                "add_to_budget_form": add_to_budget_form
            }
        )

    def post(self, request):
        budget = self.request.user.profile.budget
        income = request.POST.get("income")
        budget.total_budget = float(budget.total_budget) + float(income)
        budget.save()
        return self.get(request)


class SubmitableLoginView(LoginView):
    template_name = "form.html"
    success_url = reverse_lazy("home")


class SubmitableSignUpView(CreateView):
    form_class = SignUpForm
    template_name = "form.html"
    success_url = reverse_lazy("login")


class SubmittablePasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, PasswordChangeView):
    template_name = "form.html"
    success_url = reverse_lazy("home")
    permission_required = "viewer.change_profile"


class WelcomeView(TemplateView):
    template_name = "home.html"


class ExpenceDetailView(PermissionRequiredMixin, DetailView):
    model = Expence
    template_name = "expence_detail.html"
    success_url = reverse_lazy("expence_detail")
    permission_required = "viewer.view_expence"


class CategoryDetailView(PermissionRequiredMixin, View):
    model = Expence
    success_url = reverse_lazy("category_detail")
    permission_required = "viewer.view_expence"

    def get(self, request, category_short):
        budget = self.request.user.profile.budget
        all_expenses = Expence.objects.filter(budget=budget)
        category_expenses = all_expenses.filter(category=category_short)
        category = category_short
        total_expenses = 0
        total_category_expenses = 0
        total_budget = self.request.user.profile.budget.total_budget

        for expense in all_expenses:
            total_expenses += expense.value

        for expense in category_expenses:
            total_category_expenses += expense.value

        category_to_all = round(total_category_expenses / total_expenses, 2)
        category_to_budget = round(total_category_expenses / total_budget, 2)

        return render(
            request, template_name="category_detail.html",
            context={
                "budget": budget,
                "all_expenses": all_expenses,
                "category_expenses": category_expenses,
                "category": category,
                "category_to_all": category_to_all,
                "category_to_budget": category_to_budget,
                "total_category_expenses": total_category_expenses
            }
        )


class DeleteProfileView(PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "delete_profile.html"
    success_url = reverse_lazy("welcome")
    permission_required = "viewer.delete_profile"


class EditProfileView(PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "form.html"
    success_url = reverse_lazy("home")
    permission_required = "viewer.change_profile"

    def get_object(self, queryset=None):
        profile_id = self.request.user.profile.id
        return get_object_or_404(Profile, id=profile_id)


class EditBudgetView(PermissionRequiredMixin, UpdateView):
    form_class = UpdateBudgetForm
    # fields = ["name", "total_budget"]
    template_name = "edit_budget.html"
    success_url = reverse_lazy("home")
    permission_required = "viewer.change_budget"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        budget_id = self.request.user.profile.budget.id
        return get_object_or_404(Budget, id=budget_id)

    def form_valid(self, form):
        return super().form_valid(form)
