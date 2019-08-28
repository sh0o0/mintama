import json
import logging

from django.shortcuts import render, resolve_url
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as SuperLoginView,
    LogoutView as SuperLogoutView,
    PasswordChangeForm,
    PasswordChangeDoneView
)
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse_lazy
from rest_framework import viewsets
from social_django.models import UserSocialAuth

from .serializers import UserSerializer
from .forms import SignupForm, EntryUserDetailForm, MainlyLearningFormset, LoginForm, CheckUsernameForm, CheckPasswordForm


logger = logging.getLogger(__name__)
User = get_user_model()


class SignupView(generic.CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('user:entry_user_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_form'] = SignupForm()
        return context

    def form_valid(self, form):
        result = super().form_valid(form)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(self.request, auth_user)
            logger.info('complete User create and login User:%s', auth_user)
        return result


class EntryUserDetailView(generic.FormView):
    template_name = 'entry_user_detail.html'
    form_class = EntryUserDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry_user_detail_form'] = EntryUserDetailForm()
        context['mainly_learning_formset'] = MainlyLearningFormset()
        return context


class EntryUserDetailConfirmView(generic.FormView):
    form_class = EntryUserDetailForm

    def post(self, request, *args, **kwargs):
        super_result = super().post(request, *args, **kwargs)
        return super_result

    def form_valid(self, form):
        logger.info('EntryUserDetailConfirmView is valid True')
        user = self.request.user
        formset = MainlyLearningFormset(self.request.POST, instance=user)
        if formset.is_valid():
            formset.save()
        forms = {'entry_user_detail_form': form, 'mainly_learning_formset': formset}
        return render(self.request, 'entry_user_detail_confirm.html', forms)

    def form_invalid(self, form):
        logger.info('EntryUserDetailConfirmView is valid False')
        formset = MainlyLearningFormset(self.request.POST)
        forms = {'entry_user_detail_form': form, 'mainly_learning_formset': formset}
        return render(self.request, 'entry_user_detail.html', forms)


class AddUserDetailView(generic.UpdateView):
    model = User
    form_class = EntryUserDetailForm
    success_url = reverse_lazy('user:top')

    def get_object(self, queryset=None):
        user_id = self.request.user.id
        logger.info('AddUserDetailView def:get_object user_id:%s', user_id)
        return User.objects.get(id=user_id)


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


def check_form(request, CheckForm, server_form_name, client_form_name=None):
    logger.info('start def:check_form(%s, %s)', server_form_name, client_form_name)
    if client_form_name is None:
        client_form_name = server_form_name

    request_data = json.loads(request.body)
    data = {server_form_name: request_data[client_form_name]}
    form = CheckForm(data)
    valid_result = {}
    if form.is_valid():
        valid_result['available'] = True
    else:
        errors = json.loads(form.errors.as_json(), encoding='utf-8')
        valid_result['available'] = False
        valid_result['errors'] = []
        for error in errors[server_form_name]:
            valid_result['errors'].append(error['message'])
    logger.info('end def:check_form result: %s', valid_result)
    return JsonResponse(valid_result)


def check_username(request):
    return check_form(request, CheckUsernameForm, 'username')


def check_password(request):
    return check_form(request, CheckPasswordForm, 'password', 'password1')


#TODO:非同期にユーザー登録を実装
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             pass
#         else:
#             some_errors = json.loads(form.errors.as_json(), encoding='utf-8')
#             error_message = form.error_messages
#             some_errors.update(error_message)
#     content = {}
#     content['form'] = SignupForm()
#     return render(request, 'signup.html', content)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

