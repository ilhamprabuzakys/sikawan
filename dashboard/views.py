from datetime import datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from users.models import Satker
from masters.models import Kabupaten, Kecamatan, Provinsi, DBDesa, ProvinsiAllRawan

class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/dashboard_index.html'
    
    def get(self, request):
        context = {
            'list_provinsi': Provinsi.objects.all(),
        }
        
        # ======= Daftar Tahun =======
        tahun_saat_ini = datetime.now().year
        tahun = tahun_saat_ini - 1
        tahun_sebelumnya = tahun_saat_ini - 2
        context['tahun'] = tahun
        context['tahun_sebelumnya'] = tahun_sebelumnya
        list_year = [tahun, tahun_sebelumnya, 2021]
        context['list_year'] = list_year
        
        list_status = [
                {'label': 'Bahaya', 'value': 'BAHAYA'},
                {'label': 'Waspada', 'value': 'WASPADA'},
                {'label': 'Siaga', 'value': 'SIAGA'},
                {'label': 'Aman', 'value': 'AMAN'},
        ]
        context['list_status'] = list_status
            
        if request.user.profile.role == 'bnnp':
            provinsi_id = self.request.user.profile.satker.provinsi.pk
            context['desa_count'] = DBDesa.objects.filter(provinsi=provinsi_id).count()
            context['list_kabupaten'] = Kabupaten.objects.filter(provinsi=provinsi_id)
        if request.user.profile.role == 'bnnk':
            kabupaten_id = self.request.user.profile.satker.kabupaten.pk
            context['desa_count'] = DBDesa.objects.filter(kabupaten=kabupaten_id).count()
            context['list_kecamatan'] = Kecamatan.objects.filter(kabupaten=kabupaten_id)
        elif request.user.is_staff and request.user.is_superuser: # Superadmin
            context['desa_count'] = DBDesa.objects.count()
        
        return render(request, self.template_name, context)
    
class ProfilView(LoginRequiredMixin, View):
    template_name = "dashboard/pengaturan/profile.html"
    
    def get(self, request):
        user = self.request.user
        context = { "list_satker": Satker.objects.filter(nama_satker__contains='BNNP').order_by('nama_satker') }
        
        return render(request, self.template_name, context)
    
class KeamananView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/pengaturan/keamanan.html'
