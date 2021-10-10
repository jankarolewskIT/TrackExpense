from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, View, UpdateView

from viewer.forms import SignUpForm, CreateExpenseForm, UpdateExpenseForm, UpdateBudgetForm, UpdateProfileForm, \
    UpdateTotalBudgetForm, FormPasswordChange
from viewer.models.budget import Budget, Expence
from viewer.models.profile import Profile


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

    def get_form_kwargs(self):
        kwargs = super(ExpenseEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        self.request.user.profile.budget.current_budget()
        return super().form_valid(form)


def expense_delete(request, pk):
    instance = get_object_or_404(Expence, id=pk)
    budget = request.user.profile.budget
    # budget.total_budget += instance.value
    instance.delete()
    # budget.save()
    return redirect("home")


class ExpenseStatView(View):
    def get(self, request):
        budget_value = self.request.user.profile.budget.total_budget

        expenses = Expence.objects.filter(budget=self.request.user.profile.budget)

        transport_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="TR")
        category_transport = transport_query[0].category

        entertainment_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="ET")
        category_entertainment = entertainment_query[0].category

        health_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="PH")
        category_health = health_query[0].category

        clothes_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="CT")
        category_clothes = clothes_query[0].category

        food_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="FD")
        category_food = food_query[0].category

        accommodation_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="AD")
        category_accommodation = accommodation_query[0].category

        other_query = Expence.objects.filter(budget=self.request.user.profile.budget).filter(category="OT")
        category_other = other_query[0].category

        sum_all_expences = sum(map(lambda x: x.value, expenses))

        # Transport Stat
        sum_transport = sum(map(lambda x: x.value, transport_query))
        transport_in_budget = round(sum_transport / budget_value * 100, 2)

        # Entertainment Stat
        sum_entertainment = sum(map(lambda x: x.value, entertainment_query))
        entertainment_in_budget = round(sum_entertainment / budget_value * 100, 2)

        # Health Stat
        sum_health = sum(map(lambda x: x.value, health_query))
        health_in_budget = round(sum_health / budget_value * 100, 2)

        # Clothes Stat
        sum_clothes = sum(map(lambda x: x.value, clothes_query))
        clothes_in_budget = round(sum_clothes / budget_value * 100, 2)

        # Food Stat
        sum_food = sum(map(lambda x: x.value, food_query))
        food_in_budget = round(sum_food / budget_value * 100)
        # Accommodation Stat
        sum_accommodation = sum(map(lambda x: x.value, accommodation_query))
        accommodation_in_budget = round(sum_accommodation / budget_value * 100, 2)

        # Other Stat
        sum_other = sum(map(lambda x: x.value, other_query))
        other_in_budget = round(sum_other / budget_value * 100, 2)

        saves = budget_value - sum_all_expences
        saves_in_budget = round(saves / budget_value * 100, 2)

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
                "sum_other": sum_other,
                "transport_in_budget": transport_in_budget,
                "entertainment_in_budget": entertainment_in_budget,
                "health_in_budget": health_in_budget,
                "clothes_in_budget": clothes_in_budget,
                "food_in_budget": food_in_budget,
                "accommodation_in_budget": accommodation_in_budget,
                "other_in_budget": other_in_budget,
                "saves_in_budget": saves_in_budget,
                "category_transport": category_transport,
                "category_entertainment": category_entertainment,
                "category_health": category_health,
                "category_clothes": category_clothes,
                "category_food": category_food,
                "category_accommodation": category_accommodation,
                "category_other": category_other


            }
        )


class ProfileView(LoginRequiredMixin, View):
    model = Expence

    # def listing(self, request):
    #     expense_list =

    def get(self, request):
        categories = [category[1] for category in Expence.Catagory.choices]
        budget = self.request.user.profile.budget
        queryset = Expence.objects.filter(budget=budget).filter(is_archive=False).order_by("-id")
        paginator = Paginator(queryset, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        form = CreateExpenseForm
        add_to_budget_form = UpdateTotalBudgetForm

        return render(
            request, template_name="profile.html",
            context={
                "expenses": queryset,
                "budget": budget,
                "categories": categories,
                "form": form,
                "add_to_budget_form": add_to_budget_form,
                "page_obj": page_obj

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
    template_name = "sign_up.html"
    success_url = reverse_lazy("login")


class SubmittablePasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, PasswordChangeView):
    template_name = "password_change.html"
    success_url = reverse_lazy("home")
    permission_required = "viewer.change_profile"
    form_class = FormPasswordChange


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

        Category = {
            "TR": "Transport",
            "ET": "Entertainment",
            "PH": "Health",
            "CT": "Clothes",
            "FD": "Food",
            "AD": "Accommodation",
            "OT": "Others"}

        category = Category[category_short]
        t = 0
        # category = Expence.Catagory.choices[0][1]

        total_expenses = 0
        total_category_expenses = 0
        total_budget = self.request.user.profile.budget.total_budget

        for expense in all_expenses:
            total_expenses += expense.value

        for expense in category_expenses:
            total_category_expenses += expense.value

        category_to_all = round(total_category_expenses / total_expenses * 100, 2)
        category_to_budget = round(total_category_expenses / total_budget * 100, 2)

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


class DeleteProfileView(PermissionRequiredMixin, View):
    model = User
    template_name = "delete_profile.html"
    success_url = reverse_lazy("welcome")
    permission_required = "viewer.delete_profile"

    def get(self, request):
        profile = self.request.user.profile
        object = User.objects.get(profile=profile)
        return render(
            request, template_name="delete_profile.html",
            context={
                "object": object
            }
        )

    def post(self, request):
        profile = self.request.user.profile
        user = User.objects.get(profile=profile)
        user.delete()

        return redirect("welcome")


class EditProfileView(PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "edit_profile.html"
    success_url = reverse_lazy("home")
    permission_required = "viewer.change_profile"

    def get_object(self, queryset=None):
        profile_id = self.request.user.profile.id
        return get_object_or_404(Profile, id=profile_id)


class EditBudgetView(PermissionRequiredMixin, UpdateView):
    form_class = UpdateBudgetForm
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
