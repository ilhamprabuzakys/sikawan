import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.mixins import SuperAdminMixin
from masters.models import Provinsi
from users.models import Satker, SatkerBNNK, SatkerBNNP

class UsersBaseView(LoginRequiredMixin, SuperAdminMixin):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class KelolaPenggunaView(UsersBaseView, TemplateView):
    template_name = 'users/list_user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_satker_bnnp'] = SatkerBNNP.objects.order_by('nama_satker')
        context['list_satker_bnnk'] = SatkerBNNK.objects.order_by('nama_satker')
        context['list_provinsi'] = Provinsi.objects.order_by('nama_provinsi')
        return context
    