from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.contrib.auth import authenticate

from . import forms

class SignInView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = forms.LoginForm
    
    def get_form_kwargs(self):
        kwargs = super(SignInView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_user(self):
        return authenticate(self.request, username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
    
    # def form_invalid(self, form):
    #     response = super().form_invalid(form)
    #     messages.error(self.request, 'Masukan yang Anda berikan tidak valid. Harap periksa kembali.')
    #     return response
    
    # def get_success_url(self):
    #     next_url = self.request.GET.get('next', None)
        
    #     if next_url:
    #         return next_url
    #     else:
    #         return redirect('/admin/')

class SignOutView(LogoutView):
    next_page = 'logged_out'
    