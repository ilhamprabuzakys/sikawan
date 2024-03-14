from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers

from users.serializers import UserSerializer

from . import models

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provinsi
        fields = [
            "id",
            "provinsi",
            "nama_provinsi",
            "latitude",
            "longitude",
        ]
    
class RegencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Kabupaten
        fields = (
            'id', 'nama_kabupaten', 'kabupaten', 'provinsi'
        )
        
        datatables_always_serialize = fields
        
class DistrictSerializer(serializers.ModelSerializer):
    nama_provinsi = serializers.CharField(source='kabupaten.provinsi.nama_provinsi', read_only=True, default='-')
    nama_kabupaten = serializers.CharField(source='kabupaten.nama_kabupaten', read_only=True, default='-')
    
    class Meta:
        model = models.Kecamatan
        fields = [
            "id",
            "kecamatan",
            "kabupaten",
            "nama_kecamatan",
            "nama_provinsi",
            "nama_kabupaten",
        ]
        
class DesaSerializer(serializers.ModelSerializer):
    kawasan_rawan = serializers.SerializerMethodField()
    
    class Meta:
        model = models.DBDesa
        fields  = '__all__'
        datatables_always_serialize = ['desa', 'kawasan_rawan']
        
    def get_kawasan_rawan(self, obj):
        kawasan_rawan = {}
        upper_year = datetime.now().year + 1
        for tahun in range(2021, upper_year):
            data_kawasan_rawan = models.KawasanRawan.objects.filter(tahun=tahun, desa=obj.desa).first()
            
            if data_kawasan_rawan:
                kawasan_rawan[tahun] = {
                    'id': data_kawasan_rawan.pk,
                    'status': data_kawasan_rawan.status,
                    'keterangan': '-' if not data_kawasan_rawan.keterangan else data_kawasan_rawan.keterangan
                }
            else:
                kawasan_rawan[tahun] = None
        return kawasan_rawan
            
class KawasanMinifiedSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = models.KawasanRawan
        fields = '__all__'

class KawasanRawanSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=True)
    wilayah = serializers.SerializerMethodField()
    
    class Meta:
        model = models.KawasanRawan
        fields = '__all__'
    
    def get_wilayah(self,obj):
        desa = models.DBDesa.objects.get(desa=int(obj.desa.id))
        return DesaSerializer(desa).data

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Desa
        fields = [
            "id",
            "desa",
            "kecamatan",
            "nama_desa",
            "created_at",
            "updated_at",
        ]
        
        datatables_always_serialize = fields

class ProvinsiRawanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProvinsiRawan
        fields = [
            "id",
            "provinsi",
            "nama_provinsi",
            "siaga",
            "bahaya",
            "waspada",
            "aman",
            "tahun"
        ]

class ProvinsiRawanGeomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProvinsiRawanGeom
        fields = [
            "id",
            "geom",
            "tahun",
        ]


# Total : Untuk keperluan menampilkan data jumlah kawasan_rawan dari masing-masing tahun
class ProvinsiAllRawanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProvinsiAllRawan
        fields = ['nama_provinsi', 'provinsi_id', 'total_desa']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)

        kawasan_rawan = {}
        for tahun in [2021, 2022, 2023]:
            kawasan_rawan[tahun] = {
                "total": getattr(instance, f"total_{tahun}"),
                "bahaya": getattr(instance, f"bahaya_{tahun}"),
                "waspada": getattr(instance, f"waspada_{tahun}"),
                "siaga": getattr(instance, f"siaga_{tahun}"),
                "aman": getattr(instance, f"aman_{tahun}"),
            }

        data["kawasan_rawan"] = kawasan_rawan

        return data

class KabupatenAllRawanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KabupatenAllRawan
        fields = ['nama_provinsi', 'nama_kabupaten', 'provinsi_id', 'kabupaten_id', 'total_desa']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)

        kawasan_rawan = {}
        for tahun in [2021, 2022, 2023]:
            kawasan_rawan[tahun] = {
                "total": getattr(instance, f"total_{tahun}"),
                "bahaya": getattr(instance, f"bahaya_{tahun}"),
                "waspada": getattr(instance, f"waspada_{tahun}"),
                "siaga": getattr(instance, f"siaga_{tahun}"),
                "aman": getattr(instance, f"aman_{tahun}"),
            }

        data["kawasan_rawan"] = kawasan_rawan

        return data

class KecamatanAllRawanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KecamatanAllRawan
        fields = ['nama_provinsi', 'nama_kabupaten', 'nama_kecamatan', 'provinsi_id', 'kabupaten_id', 'kecamatan_id', 'total_desa']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)

        kawasan_rawan = {}
        for tahun in [2021, 2022, 2023]:
            kawasan_rawan[tahun] = {
                "total": getattr(instance, f"total_{tahun}"),
                "bahaya": getattr(instance, f"bahaya_{tahun}"),
                "waspada": getattr(instance, f"waspada_{tahun}"),
                "siaga": getattr(instance, f"siaga_{tahun}"),
                "aman": getattr(instance, f"aman_{tahun}"),
            }

        data["kawasan_rawan"] = kawasan_rawan

        return data

class DesaAllRawanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DesaAllRawan
        fields  = '__all__'

class TotalKawasanKawanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TotalKawasanKawan
        fields = '__all__'

# Desa untuk kebutuhan select2
class DaftarDesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DesaView
        fields = [
            "id",
            "desa_lengkap",
            "desa",
            "kecamatan",
            "propinsi",
            "desa_id",
        ]

# Listing for filter only
class ListRegencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Kabupaten
        fields = [
            "id",
            "nama_kabupaten",
            "kabupaten",
        ]

class ListDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Kecamatan
        fields = [
            "id",
            "nama_kecamatan",
            "kecamatan",
        ]

class ListVillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Desa
        fields = [
            "id",
            "nama_desa",
            "desa",
        ]