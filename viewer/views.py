from django.views.generic import TemplateView, ListView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import render

from viewer.models.expence import Expence


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
        expences = Expence.objects.filter(category=category_short)
        return render(
            request, template_name="category_detail.html",
            context={
                "expences": expences
            }
        )
