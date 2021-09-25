from django.views.generic import TemplateView
from django.urls import reverse_lazy


class ProfileView(TemplateView):
    template_name = "base.html"
    reverse_lazy = "home"

