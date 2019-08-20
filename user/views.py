import os
import logging

from django.shortcuts import render, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as SuperLoginView,
    LogoutView as SuperLogoutView,
    PasswordChangeForm,
    PasswordChangeDoneView
)
from django.views import generic
from django.urls import reverse_lazy
from django.conf import settings
from django.http.response import HttpResponse
from rest_framework import viewsets
from social_django.models import UserSocialAuth

from .models import User
from .serializers import UserSerializer
from .forms import RegistrationForm, LoginForm


logger = logging.getLogger(__name__)


class RegistrationView(generic.CreateView):
    template_name = 'registration.html'
    model = User
    form_class = RegistrationForm


class LoginView(SuperLoginView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'


class LogoutView(SuperLogoutView):
    template_name = 'logout.html'


class TopView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'top.html'
    redirect_field_name = 'redirect_to'


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = ['id', 'username', 'email']
