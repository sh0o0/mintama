import json
import logging

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .forms import SignupForm, CheckUsernameForm, CheckPasswordForm


logger = logging.getLogger(__name__)
User = get_user_model()


#Django Template
class LoginOrSignupView(generic.TemplateView):
    template_name = 'login_or_signup.html'


class SignupView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('accounts:home')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class IndexView(generic.TemplateView):
    template_name = 'index.html'



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


@csrf_exempt
def check_username(request):
    return check_form(request, CheckUsernameForm, 'username')


@csrf_exempt
def check_password(request):
    return check_form(request, CheckPasswordForm, 'password', 'password1')
