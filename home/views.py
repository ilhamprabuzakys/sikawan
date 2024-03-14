from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from literasi.models import Literasi
from masters.models import Provinsi

class BerandaView(TemplateView):
    template_name = 'home/beranda.html'
    
class InfoPengenalanView(TemplateView):
    template_name = 'home/info/pengenalan.html'

class InfoFAQView(TemplateView):
    template_name = 'home/info/faq.html'

class InfoMediaSosialView(TemplateView):
    template_name = 'home/info/media_sosial.html'

class InfoLiterasiView(TemplateView):
    template_name = 'home/info/literasi.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tahun = int(datetime.now().year)
        
        context['tahun'] = tahun
        context['list_literasi'] = Literasi.objects.all()
        
        return context
    
class KawasanRawanView(TemplateView):
    template_name = 'home/kawasan_rawan/kawasan_rawan.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        list_status_kerawanan = [
            {
                "label": "Bahaya",
                "value": "bahaya"
            },
            {
                "label": "Waspada",
                "value": "waspada"
            },
            {
                "label": "Siaga",
                "value": "siaga"
            },
            {
                "label": "Aman",
                "value": "aman"
            },
        ]
        
        
        context['list_status_kerawanan'] = list_status_kerawanan
        
        return context

class DetailKawasanRawanView(TemplateView):
    template_name = 'home/kawasan_rawan/detail_kawasan_provinsi.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tahun = int(kwargs.get('tahun', 2023))
        id_provinsi = int(kwargs.get('provinsi', 32))
        provinsi = Provinsi.objects.filter(pk=id_provinsi).first()

        context['tahun'] = tahun
        context['provinsi'] = provinsi
        
        return context


# Custom Error Pages
def handler_404(request, exception):
    template_name = 'errors/404.html'
    return render(request, template_name)

def handler_500(request, exception=None):
    template_name = 'errors/500.html'
    return render(request, template_name)

# Redirect URL
def redirect_to_login(request):
    return redirect(reverse('accounts:login'))

