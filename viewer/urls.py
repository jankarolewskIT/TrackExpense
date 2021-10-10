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
from django.contrib.auth.views import (
    PasswordResetView, PasswordChangeDoneView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

from viewer.views import (
    ProfileView, ExpenceDetailView, CategoryDetailView,
    EditBudgetView, ExpenseCreateView,
    SubmittablePasswordChangeView,
    EditProfileView, DeleteProfileView, ExpenseStatView, expense_delete, ExpenseEditView
)

urlpatterns = [
    path('', ProfileView.as_view(), name="home"),
    path('profile/edit/<pk>', EditProfileView.as_view(), name="edit_profile"),
    path('profile/delete', DeleteProfileView.as_view(), name="delete_profile"),
    path('change/passowrd', SubmittablePasswordChangeView.as_view(), name="change_password"),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('expence/detail/<pk>/', ExpenceDetailView.as_view(), name="expence_detail"),
    path('budget/edit/<pk>', EditBudgetView.as_view(), name="edit_budget"),
    path('category/detail/<category_short>/', CategoryDetailView.as_view(), name="category_detail"),
    path('expense/add', ExpenseCreateView.as_view(), name="add_expense"),
    path('expense/edit/<pk>', ExpenseEditView.as_view(), name="edit_expense"),
    path('expense/delete/<pk>', expense_delete, name="delete_expense"),
    path('expense/stat', ExpenseStatView.as_view(), name="stat_expense"),

]
