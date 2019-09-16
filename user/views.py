import json
import logging

from django.shortcuts import render, resolve_url
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordChangeForm,
    PasswordChangeDoneView
)
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from social_django.models import UserSocialAuth

from .forms import SignupForm, CheckUsernameForm, CheckPasswordForm
from .models import Category, Reference, Portfolio
from .permissions import IsAdminOrReadOnly
from .serializers import UserFilter, UserSerializer, CategorySerializer, ReferenceSerializer, PortfolioSerializer


logger = logging.getLogger(__name__)
User = get_user_model()


class BaseViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        if kwargs['pk'] == 'my!own!info':
            logger.debug('user api my own info')
            user = request.user
            serializer = self.get_serializer(user)
            print(serializer.data)
            return Response(serializer.data)

        logger.info('user api %s', kwargs['pk'])
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info('start user update')
        if kwargs['pk'] == 'my!own!info':
            instance = self.request.user
        else:
            instance = self.get_object()

        print(request.data)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#API
class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    permission_classes = [IsAuthenticated]


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ReferenceViewSet(BaseViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]


class PortfolioViewSet(BaseViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]


#Django Template
class LoginOrSignupView(generic.TemplateView):
    template_name = 'login_or_signup.html'


class SignupView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('user:home')

    def form_valid(self, form):
        logger.debug('signup form valid')
        super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(self.request, auth_user)
            logger.info('complete User create and login User:%s', auth_user)

        return JsonResponse({})

    def form_invalid(self, form):
        errors = dict(form.errors.items())
        logger.debug('signup form invalid %s', errors)
        return JsonResponse(errors)


class LoginView(BaseLoginView):

    def form_valid(self, form):
        login(self.request, form.get_user())
        return JsonResponse({})

    def form_invalid(self, form):
        errors = dict(form.errors.items())
        if errors.get('__all__', None):
            errors['non_field_errors'] = errors.pop('__all__')
        return JsonResponse(errors)


class LogoutView(BaseLogoutView):
    template_name = 'logout.html'


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'
    redirect_field_name = 'redirect_to'


class IndexView(generic.TemplateView):
    template_name = 'index.html'
    redirect_field_name = 'redirect_to'


def encrypt_password(target_dict):
    #keyに"password"が含まれている場合、"*"へ変換
    #暗号化された辞書コピーを返す
    result_dict = {}
    for key, value in target_dict.items():
        if 'password' in key:
            result_dict[key] = '*' * len(value)
        else:
            result_dict[key] = value

    return result_dict


#Check Form
def check_form(request, check_form_class, server_form_name, client_form_name=None):
    logger.debug('start check_form(%s)', server_form_name)
    if client_form_name is None:
        client_form_name = server_form_name

    #バイト文字列をutfへ変換
    request_json= json.loads(request.body)

    data = {server_form_name: request_json[client_form_name]}
    form = check_form_class(data)
    if form.is_valid():
        logger.debug('check_form valid %s', encrypt_password(request_json))
        return JsonResponse({})
    else:
        errors = dict(form.errors.items())
        if errors.get('password', None):
            errors['password1'] = errors.pop('password')
        logger.info('check_form invalid %s', errors)
        return JsonResponse(errors)


def check_username(request):
    return check_form(request, CheckUsernameForm, 'username')


def check_password(request):
    return check_form(request, CheckPasswordForm, 'password', 'password1')
