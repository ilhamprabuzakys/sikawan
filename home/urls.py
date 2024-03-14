from django.conf import settings
from django.urls import include, path

from . import views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    path('', views.BerandaView.as_view(), name="index"),
    
    # Info
    path('info/pengenalan/', views.InfoPengenalanView.as_view(), name="info_pengenalan"),
    path('info/faq/', views.InfoFAQView.as_view(), name="info_faq"),
    path('info/media-sosial/', views.InfoMediaSosialView.as_view(), name="info_media_sosial"),
    path('info/literasi/', views.InfoLiterasiView.as_view(), name="info_literasi"),
    
    # Kawasan rawan
    path('kawasan-rawan/', views.KawasanRawanView.as_view(), name='kawasan_rawan'),
    path('kawasan-rawan/<int:tahun>/<int:provinsi>/', views.DetailKawasanRawanView.as_view(), name='detail_kawasan_rawan'),
    
    # Redirecting user
    path('login/', views.redirect_to_login, name="redirect_to_login"),
]
