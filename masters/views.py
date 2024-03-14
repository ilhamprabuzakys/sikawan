from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render
from django.urls import reverse
# from django.views import View
from django.views.generic import TemplateView

from . import models
from core.mixins import AdminMixin, SuperAdminMixin

class MasterBaseView(LoginRequiredMixin):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Daftar Tahun
        tahun_saat_ini = datetime.now().year
        tahun = tahun_saat_ini - 1
        tahun_sebelumnya = tahun_saat_ini - 2
        
        context['tahun_saat_ini'] = tahun_saat_ini
        context['tahun'] = tahun
        context['tahun_sebelumnya'] = tahun_sebelumnya
    
        list_year = [tahun_saat_ini, tahun, tahun_sebelumnya, 2021]
        context['list_year'] = list_year
        
        return context

class MastersListView(MasterBaseView, TemplateView):
    template_name = 'masters/kawasan_rawan/list/list_kawan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Mendapatkan tahun dari URL (jika menggunakan URL pattern)
        tahun = int(kwargs.get('tahun', 2024))
        tahun_sebelumnya = tahun - 1

        list_status = [
            {'label': 'Bahaya', 'value': 'bahaya'},
            {'label': 'Waspada', 'value': 'waspada'},
            {'label': 'Siaga', 'value': 'siaga'},
            {'label': 'Aman', 'value': 'aman'},
        ]

        context['list_status'] = list_status
        context['tahun'] = tahun
        context['tahun_sebelumnya'] = tahun_sebelumnya
        
        context['list_provinsi'] = models.Provinsi.objects.all()

        return context

class TabelSebaranKawasanRawanListView(MasterBaseView, SuperAdminMixin, TemplateView):
    template_name = 'masters/tabel_sebaran/list_data_sebaran.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['jumlah_desa'] = models.DBDesa.objects.count()
        
        return context
    
class KawasanCreateView(MasterBaseView, AdminMixin, TemplateView):
    template_name = 'masters/kawasan_rawan/create/create_kawan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        list_status = [
            {'label': 'Bahaya', 'value': 'BAHAYA'},
            {'label': 'Waspada', 'value': 'WASPADA'},
            {'label': 'Siaga', 'value': 'SIAGA'},
            {'label': 'Aman', 'value': 'AMAN'},
        ]
        context['list_status'] = list_status
        
        
        if self.request.user.profile.role == 'bnnp':
            provinsi_id = self.request.user.profile.satker.provinsi.pk
            context['desa_count'] = models.DBDesa.objects.filter(provinsi=provinsi_id).count()
            context['list_kabupaten'] = models.Kabupaten.objects.filter(provinsi=provinsi_id)
        if self.request.user.profile.role == 'bnnk':
            kabupaten_id = self.request.user.profile.satker.kabupaten.pk
            context['desa_count'] = models.DBDesa.objects.filter(kabupaten=kabupaten_id).count()
            context['list_kecamatan'] = models.Kecamatan.objects.filter(kabupaten=kabupaten_id)
        elif self.request.user.is_staff and self.request.user.is_superuser: # Superadmin
            context['desa_count'] = models.DBDesa.objects.count()
        
        return context
    
class KawasanAmbilView(MasterBaseView, TemplateView):
    template_name = 'masters/kawasan_rawan/ambil/ambil_kawan.html'
    
# Untuk kebutuhan crud data wilayah (jika diperlukan)
class ListProvinsiView(MasterBaseView, TemplateView):
    template_name = 'masters/provinsi/list_provinsi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['list_provinsi'] = models.Provinsi.objects.all()
        
        return context

class ListKotaView(MasterBaseView, TemplateView):
    template_name = 'masters/kota/list_kota.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['list_kota'] = models.Kabupaten.objects.all()

        return context
        
        
class ListKecamatanView(MasterBaseView, TemplateView):
    template_name = 'masters/kecamatan/list_kecamatan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['list_kecamatan'] = models.Kecamatan.objects.all()
        
        return context
        
        
class ListDesaView(MasterBaseView, TemplateView):
    template_name = 'masters/desa/list_desa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['list_desa'] = models.Desa.objects.all()
        
        return context
        