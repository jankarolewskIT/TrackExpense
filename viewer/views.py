from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, View, UpdateView

from viewer.models.expence import Expence
from viewer.models.budget import Budget
from viewer.forms import SignUpForm, UpdateBudgetForm, CreateExpenseForm


class ExpensePopUpView(CreateView):
    form_class = CreateExpenseForm
    template_name = "profile.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    model = Expence

    def get(self, request):
        categories = [category[1] for category in Expence.Catagory.choices]
        budget = self.request.user.profile.budget
        queryset = Expence.objects.filter(budget=budget)

        return render(
            request, template_name="profile.html",
            context={
                "expenses": queryset,
                "budget": budget,
                "categories": categories
            }
        )


class SubmitableLoginView(LoginView):
    template_name = "form.html"
    success_url = reverse_lazy("home")


class SubmitableSignUpView(CreateView):
    form_class = SignUpForm
    template_name = "form.html"
    success_url = reverse_lazy("login")


class WelcomeView(TemplateView):
    template_name = "home.html"
    success_url = reverse_lazy("welcome")


class ExpenceDetailView(DetailView):
    model = Expence
    template_name = "expence_detail.html"
    success_url = reverse_lazy("expence_detail")


class CategoryDetailView(View):
    model = Expence
    success_url = reverse_lazy("category_detail")

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
                "category_to_budget": category_to_budget
            }
        )

    # def get(self, request, category_short):
    #     all_expences = Expence.objects.values_list("value")
    #     expences_query = Expence.objects.all()
    #     category_expences = Expence.objects.values_list("value").filter(category=category_short)
    #     category = category_short
    #     total_expences = 0
    #     total_category_expences = 0
    #
    #     for expence in category_expences:
    #         total_category_expences += expence[0]
    #
    #     for expence in all_expences:
    #         total_expences += expence[0]
    #
    #     total_budget = 0
    #     if len(expences_query) > 0:
    #         total_budget = expences_query[3].budget.total_budget
    #
    #     category_to_all = round(total_category_expences / total_expences, 2)
    #     category_to_budget = round(total_category_expences / total_budget, 2)
    #
    #     return render(
    #         request, template_name="category_detail.html",
    #         context={
    #             "category_to_budget": category_to_budget,
    #             "total_expences": total_expences,
    #             "category_expences": category_expences,
    #             "total_category_expences": total_category_expences,
    #             "category_to_all": category_to_all,
    #             "category": category
    #         }
    #     )


class EditBudgetView(UpdateView):
    # form_class = UpdateBudgetForm
    fields = ["name", "total_budget"]
    template_name = "edit_budget.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        budget_id = self.request.user.profile.budget.id
        return get_object_or_404(Budget, id=budget_id)

    def form_valid(self, form):
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     model = self.request.user.profile.budget
    #     return render(
    #         request, template_name="edit_budget.html",
    #         context={
    #             "model": model
    #         }
    #     )

    # def get(self, request, *args, **kwargs):
    #     budget = self.request.user.profile.budget
    #     form = UpdateBudgetForm
    #     return render(
    #         request, template_name="edit_budget.html",
    #         context={
    #             "budget": budget,
    #             "form": form
    #         }
    #     )
