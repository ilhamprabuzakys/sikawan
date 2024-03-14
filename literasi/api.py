import os
import django_filters
from django_filters.filters import Q
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from . import serializers
from . import models

class LiterasiFilter(filters.FilterSet):
    status = filters.ChoiceFilter(field_name='status', choices=models.Literasi.STATUS_CHOICES, label='Status')
    kategori = filters.ChoiceFilter(field_name='kategori', choices=models.Literasi.KATEGORI_CHOICES, label='Kategori')
    s = filters.CharFilter(method='filter_global_search', label='Global search')

    class Meta:
        model = models.Literasi
        fields = ['status', 'kategori', 's']
        order_by = ['judul', 'created_at', 'updated_at']

    def filter_global_search(self, queryset, name, value):
        return queryset.filter(
            Q(judul__icontains=value) |
            Q(status__icontains=value) |
            Q(kategori__icontains=value) |
            Q(created_by__profile__satker__nama_satker__icontains=value)
        )

class LiterasiViewSet(viewsets.ModelViewSet):
    queryset = models.Literasi.objects.all()
    serializer_class = serializers.LiterasiSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = LiterasiFilter
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        request_dokumen = self.request.data.get('dokumen', None)
        
        # Hapus dokumen saat ini jika ada perubahan dokumen dalam request
        if request_dokumen and instance.dokumen:
            if os.path.isfile(instance.dokumen.path):
                os.remove(instance.dokumen.path)

        serializer.save(updated_by=self.request.user)
    
    @action(methods=['get'], detail=True)
    def increment_unduhan(self, request, pk):
        try:
            literasi = models.Literasi.objects.get(pk=pk)
            literasi.jumlah_diunduh += 1
            literasi.save()
            return Response({"message": "Jumlah unduhan berhasil diperbarui."}, status=status.HTTP_200_OK)
        except models.Literasi.DoesNotExist:
            return Response({"message": "Literasi tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)