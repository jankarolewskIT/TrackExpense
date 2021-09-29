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
from django.contrib import admin
from django.urls import include, path
from viewer.models import Budget, Profile, Expence
from django.contrib.auth.views import LogoutView
from viewer.views import WelcomeView, SubmitableLoginView

admin.site.register(Budget)
admin.site.register(Expence)
admin.site.register(Profile)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('viewer/', include('viewer.urls')),
    path('front', WelcomeView.as_view(), name="welcome"),
    path('login', SubmitableLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
