from django.views.generic import TemplateView, ListView, DetailView, View
from django.db.models import Sum
from django.urls import reverse_lazy
from django.shortcuts import render

from viewer.models.expence import Expence
from viewer.models.budget import Budget
from viewer.models.profile import Profile


class ProfileView(ListView):
    model = Expence
    template_name = "profile.html"
    success_url = reverse_lazy("home")


class ExpenceDetailView(DetailView):
    model = Expence
    template_name = "expence_detail.html"
    success_url = reverse_lazy("expence_detail")


class CategoryDetailView(View):
    model = Expence
    success_url = reverse_lazy("category_detail")

    def get(self, request, category_short):
        all_expences = Expence.objects.values_list("value")
        expences_query = Expence.objects.all()
        category_expences = Expence.objects.values_list("value").filter(category=category_short)
        category = category_short
        total_expences = 0
        total_category_expences = 0

        for expence in category_expences:
            total_category_expences += expence[0]

        for expence in all_expences:
            total_expences += expence[0]

        total_budget = 0
        if len(expences_query) > 0:
            total_budget = expences_query[3].budget.total_budget

        category_to_all = round(total_category_expences / total_expences, 2)
        category_to_budget = round(total_category_expences / total_budget, 2)

        return render(
            request, template_name="category_detail.html",
            context={
                "category_to_budget": category_to_budget,
                "total_expences": total_expences,
                "category_expences": category_expences,
                "total_category_expences": total_category_expences,
                "category_to_all": category_to_all,
                "category": category
            }
        )
