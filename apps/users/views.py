from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from mixins.views import TitleMixin
from ..cart.models import Order
from ..users.forms import (UserChangePasswordForm, UserLoginForm,
                           UserProfileForm, UserRegisterForm)
from ..users.models import CustomUser


class ProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'users/profile.html'
    title = 'Профиль'
    form_class = UserProfileForm

    def get_success_url(self):
        self.success_url = reverse_lazy('profile', kwargs={'pk': self.request.user.id})
        return super().get_success_url()


class ChangeUserPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = UserChangePasswordForm
    title = 'Изменение пароля'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        self.success_url = reverse_lazy('profile', kwargs={'pk': self.request.user.id})
        return super().get_success_url()


class ProfileOrdersView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/orders.html'
    title = 'Заказы'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_orders'] = Order.objects.filter(user=self.request.user)
        return context


class LoginUserView(TitleMixin, LoginView):
    model = CustomUser
    template_name = 'users/login.html'
    title = 'Вход'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid() and form.errors.get('username'):
            user = CustomUser.get_user(form.cleaned_data['username_or_email'], form.cleaned_data['password'])
            if user:
                auth.login(self.request, user)
                return self.form_valid(form)
            messages.error(request, 'Неверное имя пользователя и/или пароль')
        return self.form_invalid(form)


class RegisterUserView(TitleMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    title = 'Регистрация'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя и/или пароль')
        return super(RegisterUserView, self).form_invalid(form)
