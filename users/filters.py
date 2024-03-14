from django.contrib.auth.models import User
import django_filters
from django_filters.filters import Q

from masters.models import Provinsi, Kabupaten

from . import models

class SatkerFilter(django_filters.FilterSet):
    TYPE_CHOICES = (
        ("BNNP", "BNNP"),
        ("BNNK", "BNNK"),
        ("SEMUA", "SEMUA"),
    )
    
    id_provinsi = django_filters.NumberFilter(field_name='provinsi', label='ID Provinsi')
    id_kabupaten = django_filters.CharFilter(field_name='kabupaten', label='ID Kabupaten')
    is_type = django_filters.ChoiceFilter(method='filter_is_type', label='Is TYPE', choices=TYPE_CHOICES)
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')

    class Meta:
        model = models.Satker
        fields = ['s', 'id_kabupaten', 'id_provinsi', 'nama_satker']
        
    
    def filter_is_type(self, queryset, name, value):
        if value == 'BNNP':
            return queryset.filter(Q(nama_satker__icontains='BNNP'))
        elif value == 'BNNK':
            return queryset.filter(Q(nama_satker__icontains='BNN Kabupaten') | Q(nama_satker__icontains='BNN Kota'))
        else:
            return queryset.all()
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(nama_satker__icontains=value)
        )
        
class UserFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='filter_global_search', label='Global search')
    is_active = django_filters.BooleanFilter(field_name='is_active', label='Is Active')
    satker = django_filters.NumberFilter(field_name='profile__satker', label='Satker')
    
    asal_provinsi = django_filters.ModelChoiceFilter(
        method='filter_asal_provinsi',
        queryset=Provinsi.objects.all(),
        label='Filter Asal Provinsi',
    )
    
    asal_kabupaten = django_filters.ModelChoiceFilter(
        method='filter_asal_kabupaten',
        queryset=Kabupaten.objects.all(),
        label='Filter Asal Kabupaten'
    )

    class Meta:
        model = User
        fields = ['s', 'is_active']
    
    def filter_asal_provinsi(self, queryset, name, value):
        return queryset.filter(profile__satker__provinsi=value.provinsi)
    
    def filter_asal_kabupaten(self, queryset, name, value):
        return queryset.filter(profile__satker__kabupaten=value.kabupaten)
    
    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(profile__satker__nama_satker__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(username__icontains=value) |
            Q(email__icontains=value)
        )