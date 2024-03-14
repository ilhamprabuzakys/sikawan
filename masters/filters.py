from django.db.models import Exists, OuterRef, Subquery
import django_filters
from django_filters.filters import Q

from . import models

class ProvinceFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')

    class Meta:
        model = models.Provinsi
        fields = ['s']
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_provinsi__icontains=value)
        )

class RegencyFilter(django_filters.FilterSet):
    provinsi = django_filters.CharFilter(field_name='provinsi__id', label='ID Provinsi')

    class Meta:
        model = models.Kabupaten
        fields = ['provinsi']

class DistrictFilter(django_filters.FilterSet):
    provinsi = django_filters.NumberFilter(field_name='kabupaten__provinsi', label='ID Provinsi')
    kabupaten = django_filters.CharFilter(field_name='kabupaten__id', label='ID Kabupaten')

    s = django_filters.CharFilter(method='filter_global_search', label='Global search')

    class Meta:
        model = models.Kecamatan
        fields = ['kabupaten', 'provinsi', 's']
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(kabupaten__provinsi__nama_provinsi__icontains=value) |
            Q(kabupaten__nama_kabupaten__icontains=value) |
            Q(nama_kecamatan__icontains=value)
        )

class VillageFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    provinsi = django_filters.NumberFilter(field_name='kecamatan__kabupaten__provinsi', label='ID Provinsi')
    kabupaten = django_filters.NumberFilter(field_name='kecamatan__kabupaten', label='ID Kabupaten')
    kecamatan = django_filters.NumberFilter(field_name='kecamatan', label='ID Kecamatan')
    tahun = django_filters.ChoiceFilter(method='filter_tahun', choices=models.KawasanRawan.TAHUN_CHOICES, label='Kawasan Tahun')
    status = django_filters.CharFilter(method='filter_status', label='Kawasan Status')
    
    class Meta:
        model = models.Desa
        fields = ['provinsi', 'kabupaten', 'kecamatan', 's', 'status' ]
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_desa__icontains=value) |
            Q(kecamatan__nama_kecamatan__icontains=value) |
            Q(kecamatan__kabupaten__nama_kabupaten__icontains=value) |
            Q(kecamatan__kabupaten__provinsi__nama_provinsi__icontains=value)
        )
        
    def filter_status(self, queryset, name, value):
        status, tahun = value.split('_')
        if status == 'kosong':
            # Mengecek desa yang tidak memiliki data kawasan_rawan pada tahun tertentu
            return queryset.filter(
                ~Exists(models.KawasanRawan.objects.filter(desa=OuterRef('pk'), tahun=tahun))
            )
        else:
            return queryset.filter(kawasan_rawan__status=status, kawasan_rawan__tahun=tahun).distinct()
        
class KawasanRawanFilter(django_filters.FilterSet):
    tahun = django_filters.ChoiceFilter(field_name='tahun', choices=models.KawasanRawan.TAHUN_CHOICES)
    status = django_filters.ChoiceFilter(field_name='status', choices=models.KawasanRawan.STATUS_CHOICES)
    desa = django_filters.CharFilter(field_name='desa', label='ID Desa')
    kecamatan = django_filters.CharFilter(field_name='desa_id__kecamatan', label='ID Kecamatan')
    kota = django_filters.CharFilter(field_name='desa_id__kabupaten', label="ID Kabupaten")
    provinsi = django_filters.CharFilter(field_name='desa_id__provinsi', label="ID Provinsi")

    class Meta:
        model = models.KawasanRawan
        fields = ['tahun', 'status', 'desa', 'kecamatan', 'kota', 'provinsi']
        

class DaftarDesaFilter(django_filters.FilterSet):
    provinsi = django_filters.NumberFilter(field_name='desa_id__kecamatan__kabupaten__provinsi', label='ID Provinsi')
    kabupaten = django_filters.NumberFilter(field_name='desa_id__kecamatan__kabupaten', label='ID Kabupaten')
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    
    class Meta:
        model = models.DesaView
        fields = ['s', 'provinsi']
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(desa_lengkap__icontains=value) |
            Q(kecamatan__icontains=value) |
            Q(propinsi__icontains=value)
        )
        
class DBDesaFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    provinsi = django_filters.CharFilter(field_name='provinsi', label='ID Provinsi')
    kabupaten = django_filters.CharFilter(field_name='kabupaten', label='ID Kabupaten')
    kecamatan = django_filters.CharFilter(field_name='kecamatan', label='ID Kecamatan')
    status = django_filters.CharFilter(method='filter_status', label='Kawasan Status')
    
    class Meta:
        model = models.DBDesa
        fields = ['s']
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_desa__icontains=value) |
            Q(nama_kecamatan__icontains=value) |
            Q(nama_kabupaten__icontains=value) |
            Q(nama_provinsi__icontains=value)
        )
        
    def filter_status(self, queryset, name, value):
        status, tahun = value.split('_')
        status = status.upper()
        
        if status == 'KOSONG':
            # Mengecek desa yang tidak memiliki data kawasan_rawan pada tahun tertentu
            return queryset.exclude(
                Exists(models.KawasanRawan.objects.filter(desa=OuterRef('pk'), tahun=tahun))
            )
        elif status == 'SUDAH':
            # Mencari desa berdasarkan status dan tahunnya dengan status tidak null
            return queryset.filter(
                Exists(models.KawasanRawan.objects.filter(desa=OuterRef('pk'), tahun=tahun, status__isnull=False))
            )
        else:
            # Mencari desa berdasarkan status dan tahunnya
            return queryset.filter(
                Exists(models.KawasanRawan.objects.filter(desa=OuterRef('pk'), tahun=tahun, status=status))
            )

class ProvinsiAllRawanFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    provinsi = django_filters.NumberFilter(field_name='provinsi_id', label='ID Provinsi')
    
    total_2023_range = django_filters.RangeFilter(field_name='total_2023', label='Range Total 2023')
    total_2022_range = django_filters.RangeFilter(field_name='total_2022', label='Range Total 2022')
    total_2021_range = django_filters.RangeFilter(field_name='total_2021', label='Range Total 2021')

    bahaya_2023_range = django_filters.RangeFilter(field_name='bahaya_2023', label='Range Bahaya 2023')
    waspada_2023_range = django_filters.RangeFilter(field_name='waspada_2023', label='Range Waspada 2023')
    siaga_2023_range = django_filters.RangeFilter(field_name='siaga_2023', label='Range Siaga 2023')
    aman_2023_range = django_filters.RangeFilter(field_name='aman_2023', label='Range Aman 2023')

    bahaya_2022_range = django_filters.RangeFilter(field_name='bahaya_2022', label='Range Bahaya 2022')
    waspada_2022_range = django_filters.RangeFilter(field_name='waspada_2022', label='Range Waspada 2022')
    siaga_2022_range = django_filters.RangeFilter(field_name='siaga_2022', label='Range Siaga 2022')
    aman_2022_range = django_filters.RangeFilter(field_name='aman_2022', label='Range Aman 2022')

    bahaya_2021_range = django_filters.RangeFilter(field_name='bahaya_2021', label='Range Bahaya 2021')
    waspada_2021_range = django_filters.RangeFilter(field_name='waspada_2021', label='Range Waspada 2021')
    siaga_2021_range = django_filters.RangeFilter(field_name='siaga_2021', label='Range Siaga 2021')
    aman_2021_range = django_filters.RangeFilter(field_name='aman_2021', label='Range Aman 2021')
    
    class Meta:
        model = models.ProvinsiAllRawan
        fields = ['s']

    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_provinsi__icontains=value) |
            Q(provinsi_id__icontains=value)
        )

class KabupatenAllRawanFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    provinsi = django_filters.NumberFilter(field_name='provinsi_id', label='ID Provinsi')
    kabupaten = django_filters.NumberFilter(field_name='kabupaten_id', label='ID Kabupaten')
    
    total_2023_range = django_filters.RangeFilter(field_name='total_2023', label='Range Total 2023')
    total_2022_range = django_filters.RangeFilter(field_name='total_2022', label='Range Total 2022')
    total_2021_range = django_filters.RangeFilter(field_name='total_2021', label='Range Total 2021')

    bahaya_2023_range = django_filters.RangeFilter(field_name='bahaya_2023', label='Range Bahaya 2023')
    waspada_2023_range = django_filters.RangeFilter(field_name='waspada_2023', label='Range Waspada 2023')
    siaga_2023_range = django_filters.RangeFilter(field_name='siaga_2023', label='Range Siaga 2023')
    aman_2023_range = django_filters.RangeFilter(field_name='aman_2023', label='Range Aman 2023')

    bahaya_2022_range = django_filters.RangeFilter(field_name='bahaya_2022', label='Range Bahaya 2022')
    waspada_2022_range = django_filters.RangeFilter(field_name='waspada_2022', label='Range Waspada 2022')
    siaga_2022_range = django_filters.RangeFilter(field_name='siaga_2022', label='Range Siaga 2022')
    aman_2022_range = django_filters.RangeFilter(field_name='aman_2022', label='Range Aman 2022')

    bahaya_2021_range = django_filters.RangeFilter(field_name='bahaya_2021', label='Range Bahaya 2021')
    waspada_2021_range = django_filters.RangeFilter(field_name='waspada_2021', label='Range Waspada 2021')
    siaga_2021_range = django_filters.RangeFilter(field_name='siaga_2021', label='Range Siaga 2021')
    aman_2021_range = django_filters.RangeFilter(field_name='aman_2021', label='Range Aman 2021')
    
    class Meta:
        model = models.KabupatenAllRawan
        fields = ['s']

    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_provinsi__icontains=value) |
            Q(nama_kabupaten__icontains=value) |
            Q(provinsi_id__icontains=value) |
            Q(kabupaten_id__icontains=value)
        )

class KecamatanAllRawanFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    provinsi = django_filters.NumberFilter(field_name='provinsi_id', label='ID Provinsi')
    kabupaten = django_filters.NumberFilter(field_name='kabupaten_id', label='ID Kabupaten')
    kecamatan = django_filters.NumberFilter(field_name='kecamatan_id', label='ID Kecamatan')
    
    total_2023_range = django_filters.RangeFilter(field_name='total_2023', label='Range Total 2023')
    total_2022_range = django_filters.RangeFilter(field_name='total_2022', label='Range Total 2022')
    total_2021_range = django_filters.RangeFilter(field_name='total_2021', label='Range Total 2021')

    bahaya_2023_range = django_filters.RangeFilter(field_name='bahaya_2023', label='Range Bahaya 2023')
    waspada_2023_range = django_filters.RangeFilter(field_name='waspada_2023', label='Range Waspada 2023')
    siaga_2023_range = django_filters.RangeFilter(field_name='siaga_2023', label='Range Siaga 2023')
    aman_2023_range = django_filters.RangeFilter(field_name='aman_2023', label='Range Aman 2023')

    bahaya_2022_range = django_filters.RangeFilter(field_name='bahaya_2022', label='Range Bahaya 2022')
    waspada_2022_range = django_filters.RangeFilter(field_name='waspada_2022', label='Range Waspada 2022')
    siaga_2022_range = django_filters.RangeFilter(field_name='siaga_2022', label='Range Siaga 2022')
    aman_2022_range = django_filters.RangeFilter(field_name='aman_2022', label='Range Aman 2022')

    bahaya_2021_range = django_filters.RangeFilter(field_name='bahaya_2021', label='Range Bahaya 2021')
    waspada_2021_range = django_filters.RangeFilter(field_name='waspada_2021', label='Range Waspada 2021')
    siaga_2021_range = django_filters.RangeFilter(field_name='siaga_2021', label='Range Siaga 2021')
    aman_2021_range = django_filters.RangeFilter(field_name='aman_2021', label='Range Aman 2021')
    
    class Meta:
        model = models.KecamatanAllRawan
        fields = ['s']

    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_provinsi__icontains=value) |
            Q(nama_kabupaten__icontains=value) |
            Q(nama_kecamatan__icontains=value) |
            Q(provinsi_id__icontains=value) |
            Q(kabupaten_id__icontains=value) |
            Q(kecamatan_id__icontains=value)
        )

class DesaAllRawanFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    provinsi = django_filters.CharFilter(field_name='provinsi', label='ID Provinsi')
    kabupaten = django_filters.CharFilter(field_name='kabupaten', label='ID Kabupaten')
    kecamatan = django_filters.CharFilter(field_name='kecamatan', label='ID Kecamatan')
    
    class Meta:
        model = models.DesaAllRawan
        fields = ['s']
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_desa__icontains=value) |
            Q(nama_kecamatan__icontains=value) |
            Q(nama_kabupaten__icontains=value) |
            Q(nama_provinsi__icontains=value)
        )