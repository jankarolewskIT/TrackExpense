"""TrackExpences URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordChangeView

from viewer.views import (
    ProfileView, ExpenceDetailView, CategoryDetailView,
    EditBudgetView, ExpenseCreateView, ExpenseDeleteView,
    ExpenseEditView, SubmittablePasswordChangeView
)

urlpatterns = [
    path('', ProfileView.as_view(), name="home"),
    path('change/passowrd', SubmittablePasswordChangeView.as_view(), name="change_password"),
    path('expence/detail/<pk>/', ExpenceDetailView.as_view(), name="expence_detail"),
    path('budget/edit/<pk>', EditBudgetView.as_view(), name="edit_budget"),
    path('category/detail/<category_short>/', CategoryDetailView.as_view(), name="category_detail"),
    path('expense/add', ExpenseCreateView.as_view(), name="add_expense"),
    path('expense/edit/<pk>', ExpenseEditView.as_view(), name="edit_expense"),
    path('expense/delete/<pk>', ExpenseDeleteView.as_view(), name="delete_expense"),
]
