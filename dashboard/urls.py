from django.urls import include, path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name="index") ,
    path('profil_saya/', views.ProfilView.as_view(), name="profil_saya") ,
    path('keamanan/', views.KeamananView.as_view(), name="keamanan") ,
]
