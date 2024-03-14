from django.urls import include, path
from rest_framework import routers
from . import api
from . import views

app_name = 'masters'

router = routers.DefaultRouter()
router.register("provinces", api.ProvinceViewSet)
router.register("regencies", api.RegencyViewSet)
router.register("districts", api.DistrictViewSet)
router.register("villages", api.VillageViewSet)
router.register("desa", api.DBDesaViewSet)
router.register("kawasan_rawan", api.KawasanRawanViewSet)
router.register("provinsi_rawan", api.ProvinsiRawanViewSet)
router.register("provinsi_rawan_geom", api.ProvinsiRawanGeomViewSet)

router.register("provinsi_all_rawan", api.ProvinsiAllRawanViewSet)
router.register("kabupaten_all_rawan", api.KabupatenAllRawanViewSet)
router.register("kecamatan_all_rawan", api.KecamatanAllRawanViewSet)
router.register("desa_all_rawan", api.DesaAllRawanViewSet)
router.register("total_kawasan_rawan", api.TotalKawasanRawanViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    
    # List Api Wilayah untuk select2 agar response timenya tidak terlalu lama, pada serializer diambil hanya beberapa saja
    path("api/v1/list_regencies/", api.RegencyListAPIView.as_view()),
    path("api/v1/list_districts/", api.DistrictListAPIView.as_view()),
    path("api/v1/list_villages/", api.VillageListAPIView.as_view()),
    path("api/v1/daftar_desa/", api.DaftarDesaAPIView.as_view()),
    
    # Data kawasan rawan (global)
    path('kawasan_rawan/<int:tahun>/', views.MastersListView.as_view(), name='kawasan_rawan'),
    path('tabel_sebaran_kawasan_rawan/', views.TabelSebaranKawasanRawanListView.as_view(), name='tabel_sebaran_kawasan_rawan'),
    
    # Masukan data kawasan
    path('kawasan_rawan/tambah/', views.KawasanCreateView.as_view(), name='kawasan_rawan_create'),
    
    # Ambil data kawasan rawan sebelumnya
    path('kawasan_rawan/ambil/', views.KawasanAmbilView.as_view(), name='kawasan_rawan_ambil'),
    
    # Data lokasi
    path('data/provinsi/', views.ListProvinsiView.as_view(), name='provinsi'),
    path('data/kota/', views.ListKotaView.as_view(), name='kota'),
    path('data/kecamatan/', views.ListKecamatanView.as_view(), name='kecamatan'),
    path('data/desa/', views.ListDesaView.as_view(), name='desa'),
]