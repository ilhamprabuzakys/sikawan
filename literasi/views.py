from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from . import models
from core.mixins import SuperAdminMixin

class LiterasiBaseView(LoginRequiredMixin, SuperAdminMixin):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LiterasiListView(LiterasiBaseView, TemplateView):
    template_name = 'literasi/list_literasi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['list_literasi'] = models.Literasi.objects.all()

        return context