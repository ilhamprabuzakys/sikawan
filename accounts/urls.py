from django.conf import settings
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from . import forms
from . import api

app_name = 'accounts'

urlpatterns = [
    path('api/update-password/', api.UpdatePasswordView.as_view(), name='update_password'),
    path('api/reset-password/', api.ResetPasswordView.as_view(), name='reset_password'),
    path('api/request-reset-password/', api.RequestResetPasswordView.as_view(), name='request_reset_password'),
    
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user = True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="accounts:logged_out"), name="logout"),
    path('logged_out/', TemplateView.as_view(template_name='accounts/logged_out.html'), name="logged_out"),
]
