import os
import logging

from django.shortcuts import render, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView as SuperLoginView,
                                       LogoutView as SuperLogoutView,
                                       PasswordChangeForm,
                                       PasswordChangeDoneView)
from django.views import generic
from django.urls import reverse_lazy
from django.conf import settings
from django.http.response import HttpResponse
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer
from .forms import RegistrationForm, LoginForm


filename = 'logfile/logger.log'
logging.basicConfig(filename=filename, level=logging.INFO, format='%(lavelname)s: %(message)s')


class NoPassFilter(logging.FileHandler):
    def filter(self, record):
        logging_message = record.getMessage()
        return 'password' not in logging_message


logger = logging.getLogger(__name__)
logger.addFilter(NoPassFilter(filename))
h = logging.FileHandler('logfile/log.log', encoding='utf8')
logger.addHandler(h)


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

    def get(self, request, *args, **kwargs):
        logger.info('info is logged')
        return super().get(request, *args, **kwargs)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = ['id', 'title', 'email',]
