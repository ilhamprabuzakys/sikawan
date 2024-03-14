import csv
import io
import re
import shutil
import pandas as pd
from rest_framework.views import APIView
from tablib import Dataset
import os
import glob
import geojson

from rest_framework import generics, parsers, viewsets, permissions, status

from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend
from rest_framework.decorators import action

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from . import models
from . import filters

from core import pagination
from django.core import serializers as jserializers
from django.http import JsonResponse
from django.views.static import serve
from django.http import HttpResponse

import json

# ======= Utama Data Desa =======
class DBDesaViewSet(viewsets.ModelViewSet):
    queryset = models.DBDesa.objects.all()
    serializer_class = serializers.DesaSerializer
    pagination_class = pagination.Page10NumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.DBDesaFilter
            
# ======= Klasifikasi Rawan =======
class ProvinsiRawanViewSet(viewsets.ModelViewSet):
    queryset = models.ProvinsiRawan.objects.all()
    serializer_class = serializers.ProvinsiRawanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tahun', 'provinsi']

# ======= Provinsi Data GEOJSON =======
class ProvinsiRawanGeomViewSet(viewsets.ModelViewSet):
    queryset = models.ProvinsiRawanGeom.objects.all()
    serializer_class = serializers.ProvinsiRawanGeomSerializer
    filter_backends = [DjangoFilterBackend]
    
# ======= Utama Kawasan Rawan =======
class KawasanRawanViewSet(viewsets.ModelViewSet):
    queryset = models.KawasanRawan.objects.all()
    serializer_class = serializers.KawasanRawanSerializer
    pagination_class = pagination.Page10NumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.KawasanRawanFilter
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False)
    def map_aman(self, request):
        prov = request.GET["prov"]
        thn = request.GET["tahun"]

        cached = os.path.isfile( os.getcwd() + "/static/geos/cache."+prov+","+thn+".aman.geojson")
        recached = request.GET.get("cache",False)
        print(recached)
        if cached and not recached:
            path = "/static/geos/cache."+prov+","+thn+".aman.geojson"
            d = serve(request, path, document_root=os.getcwd())
            return d
        else:
            kawasan = models.KawasanRawan.objects.filter(desa__provinsi=prov, tahun=thn).filter(status='AMAN')
            collection = []
            for f in kawasan:
                file = os.getcwd()  + '/static/geos/desa/' + str(f.desa.id) + '.geojson'
                try:
                    with open(file) as fl:
                        layer = geojson.load(fl)
                        ft = geojson.Feature(geometry=layer, properties={"desa": f.desa.nama_desa, 'kecamatan': f.desa.nama_kecamatan, 'kabupaten': f.desa.nama_kabupaten, 'propinsi': f.desa.nama_provinsi})
                        collection.append(ft)
                except:
                    None
                
            geo_collection = geojson.FeatureCollection(collection)
            with open(os.getcwd() + "/static/geos/cache."+prov+","+thn+".aman.geojson","w") as fl:
                geojson.dump(geo_collection,fl)
            retval = geojson.dumps(geo_collection) #json.loads(jserializers.serialize('json',kawasan))
            return Response(json.loads(retval))
    
    @action(detail=False)
    def map_bahaya(self, request):
        prov = request.GET["prov"]
        thn = request.GET["tahun"]

        cached = os.path.isfile( os.getcwd() + "/static/geos/cache."+prov+","+thn+".bahaya.geojson")
        recached = request.GET.get("cache",False)
        print(recached)
        if cached and not recached:
            path = "/static/geos/cache."+prov+","+thn+".bahaya.geojson"
            d = serve(request, path, document_root=os.getcwd())
            return d
        else:
            kawasan = models.KawasanRawan.objects.filter(desa__provinsi=prov, tahun=thn).filter(status='BAHAYA')
            collection = []
            for f in kawasan:
                file = os.getcwd()  + '/static/geos/desa/' + str(f.desa.id) + '.geojson'
                try:
                    with open(file) as fl:
                        layer = geojson.load(fl)
                        ft = geojson.Feature(geometry=layer, properties={"desa": f.desa.nama_desa, 'kecamatan': f.desa.nama_kecamatan, 'kabupaten': f.desa.nama_kabupaten, 'propinsi': f.desa.nama_provinsi})
                        collection.append(ft)
                except:
                    None
                
            geo_collection = geojson.FeatureCollection(collection)
            with open(os.getcwd() + "/static/geos/cache."+prov+","+thn+".bahaya.geojson","w") as fl:
                geojson.dump(geo_collection,fl)
            retval = geojson.dumps(geo_collection) #json.loads(jserializers.serialize('json',kawasan))
            return Response(json.loads(retval))
    
    @action(detail=False)
    def map_waspada(self, request):
        prov = request.GET["prov"]
        thn = request.GET["tahun"]

        cached = os.path.isfile( os.getcwd() + "/static/geos/cache."+prov+","+thn+".waspada.geojson")
        recached = request.GET.get("cache",False)
        print(recached)
        if cached and not recached:
            path = "/static/geos/cache."+prov+","+thn+".waspada.geojson"
            d = serve(request, path, document_root=os.getcwd())
            return d
        else:
            # kawasan = models.KawasanRawan.objects.filter(desa__provinsi = prov).filter(status='WASPADA').distinct()
            kawasan = models.KawasanRawan.objects.filter(desa__provinsi=prov, tahun=thn, status='WASPADA').distinct()
            collection = []
            for f in kawasan:
                file = os.getcwd()  + '/static/geos/desa/' + str(f.desa.id) + '.geojson'
                #print(file)
                try:
                    with open(file) as fl:
                        layer = geojson.load(fl)
                        ft = geojson.Feature(geometry=layer, properties={"desa": f.desa.nama_desa, 'kecamatan': f.desa.nama_kecamatan, 'kabupaten': f.desa.nama_kabupaten, 'propinsi': f.desa.nama_provinsi})
                        collection.append(ft)
                except:
                    None
                
            geo_collection = geojson.FeatureCollection(collection)
            with open(os.getcwd() + "/static/geos/cache."+prov+","+thn+".waspada.geojson","w") as fl:
                geojson.dump(geo_collection,fl)
            retval = geojson.dumps(geo_collection) #json.loads(jserializers.serialize('json',kawasan))
            return Response(json.loads(retval))

    @action(detail=False)
    def map_siaga(self, request):
        prov = request.GET["prov"]
        thn = request.GET["tahun"]
        # check cache
        cached = os.path.isfile( os.getcwd() + "/static/geos/cache."+prov+","+thn+".siaga.geojson")
        recached = request.GET.get("cache",False)
        print(recached)
        if cached and not recached:
            path = "/static/geos/cache."+prov+","+thn+".siaga.geojson"
            print(path)
            d = serve(request, path, document_root=os.getcwd())
            print(d)
            return d
        else:
            #desa = models.DBDesa.objects.all().filter(provinsi=propinsi)
            #desa_id = set()
            #for d in desa:
            #    desa_id.add(int(d.desa))
            kawasan = models.KawasanRawan.objects.filter(desa__provinsi=prov, tahun=thn).filter(status='SIAGA').distinct()
            collection = []
            for f in kawasan:
                file = os.getcwd()  + '/static/geos/desa/' + str(f.desa.id) + '.geojson'
                #print(file)
                try:
                    with open(file) as fl:
                        layer = geojson.load(fl)
                        ft = geojson.Feature(geometry=layer, properties={"desa": f.desa.nama_desa, 'kecamatan': f.desa.nama_kecamatan, 'kabupaten': f.desa.nama_kabupaten, 'propinsi': f.desa.nama_provinsi})
                        collection.append(ft)
                except:
                    None
                
            geo_collection = geojson.FeatureCollection(collection)
            retval = geojson.dumps(geo_collection) #json.loads(jserializers.serialize('json',kawasan))
            with open(os.getcwd() + "/static/geos/cache."+prov+","+thn+".siaga.geojson","w") as fl:
                 geojson.dump(geo_collection,fl)
            return Response(json.loads(retval))

    @action(detail=True)
    def map_provinsi(self, request, pk):
        # check cache
        tahun = request.GET.get("tahun","2023")
        cached = os.path.isfile( os.getcwd() + "/static/geos/cache.provinsi."+pk+"."+tahun+".geojson")
        recached = request.GET.get("cache",False)
        if cached and not recached:
            path = "/static/geos/cache.provinsi."+pk+"."+tahun+".geojson"
            print(path)
            d = serve(request, path, document_root=os.getcwd())
            print(d)
            return d
        else:
            collection = []
            kawasan = models.ProvinsiRawan.objects.filter(provinsi=pk).filter(tahun=tahun)
            for f in kawasan:
                file = os.getcwd()  + '/static/geos/propinsi/' + str(f.provinsi) + '.geojson'
                try:
                    with open(file) as fl:
                        layer = geojson.load(fl)
                        ft = geojson.Feature(geometry=layer, properties={'provinsi':f.nama_provinsi,'kd_prov':f.provinsi, "siaga": f.siaga, 'waspada': f.waspada, 'bahaya': f.bahaya, 'aman': f.aman})
                        collection.append(ft)
                except:
                    None
                
            geo_collection = geojson.FeatureCollection(collection)
            retval = geojson.dumps(geo_collection) #json.loads(jserializers.serialize('json',kawasan))
            with open(os.getcwd() + "/static/geos/cache.provinsi."+pk+"."+tahun+".geojson","w") as fl:
                 geojson.dump(geo_collection,fl)
            return Response(json.loads(retval))

    @action(detail=False)
    def map_provinsi_geom(self, request):
        # check cache
        tahun = request.GET.get("tahun","2023")

        collection = []
        kawasan = models.ProvinsiRawanGeom.objects.filter(tahun=tahun)
        for f in kawasan:
            #file = os.getcwd()  + '/static/geos/propinsi/' + str(f.provinsi) + '.geojson'
            #try:
            #    with open(file) as fl:
            #        layer = geojson.load(fl)
            #        ft = geojson.Feature(geometry=layer, properties={'provinsi':f.nama_provinsi,'kd_prov':f.provinsi, "siaga": f.siaga, 'waspada': f.waspada, 'bahaya': f.bahaya, 'aman': f.aman})
            collection.append(f.geom)
            
        geo_collection = geojson.FeatureCollection(collection)
        retval = geojson.dumps(geo_collection) #json.loads(jserializers.serialize('json',kawasan))
        return Response(json.loads(retval))


    def create(self, request, *args, **kwargs):
        desa_id = request.data.get('desa')
        tahun = request.data.get('tahun')
        new_status = request.data.get('status')

        existing_entry = models.KawasanRawan.objects.filter(desa_id=desa_id, tahun=tahun).first()

        # Jika data kawasan rawan dengan desa id dan tahun yang sama ditemukan
        if existing_entry:
            # Lakukan update status atau keterangan
            existing_entry_name = existing_entry.desa.nama_desa
            existing_entry_status = existing_entry.status
            
            serializer = self.get_serializer(existing_entry, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'data': serializer.data,
                'info': 'updated',
                'message': f'Data kawasan {existing_entry_name}, terjadi perubahan status dari {existing_entry_status} ke {new_status}',
                'detail': {
                    'nama_desa': existing_entry_name,
                    'status': {
                        'from': existing_entry_status,
                        'to': new_status
                    },
                }
            }, status=status.HTTP_200_OK)
        else:
            # Jika tidak ditemukan, buat instance baru dari kawasan_rawan
            return super().create(request, *args, **kwargs)
        
# =============================================
# Data Wilayah Listing
# INFO : Untuk filtering berdasarkan parent_id + lightweight serializer
# =============================================
class RegencyListAPIView(generics.ListAPIView):
    queryset = models.Kabupaten.objects.all()
    serializer_class = serializers.ListRegencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.RegencyFilter

class DistrictListAPIView(generics.ListAPIView):
    queryset = models.Kecamatan.objects.all()
    serializer_class = serializers.ListDistrictSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.DistrictFilter

class VillageListAPIView(generics.ListAPIView):
    queryset = models.Desa.objects.all()
    serializer_class = serializers.ListVillageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.VillageFilter

class DaftarDesaAPIView(generics.ListAPIView):
    queryset = models.DesaView.objects.all()
    serializer_class = serializers.DaftarDesaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.DaftarDesaFilter
    pagination_class = pagination.Page500NumberPagination
    
# =============================================
# Klasifikasi Data Kawasan Rawan - Per Wilayah
# =============================================
class ProvinsiAllRawanViewSet(viewsets.ModelViewSet):
    queryset = models.ProvinsiAllRawan.objects.all()
    serializer_class = serializers.ProvinsiAllRawanSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = pagination.Page10NumberPagination
    filterset_class = filters.ProvinsiAllRawanFilter

class KabupatenAllRawanViewSet(viewsets.ModelViewSet):
    queryset = models.KabupatenAllRawan.objects.all()
    serializer_class = serializers.KabupatenAllRawanSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = pagination.Page10NumberPagination
    filterset_class = filters.KabupatenAllRawanFilter

class KecamatanAllRawanViewSet(viewsets.ModelViewSet):
    queryset = models.KecamatanAllRawan.objects.all()
    serializer_class = serializers.KecamatanAllRawanSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = pagination.Page10NumberPagination
    filterset_class = filters.KecamatanAllRawanFilter

# ======= Fungsionalitas Import Export Kawasan Rawan Berdasarkan Total Desa Wilayah =======
class DesaAllRawanViewSet(viewsets.ModelViewSet):
    queryset = models.DesaAllRawan.objects.all()
    serializer_class = serializers.DesaAllRawanSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = pagination.Page10NumberPagination
    filterset_class = filters.DesaAllRawanFilter
    
    @action(detail=False, methods=['POST'])
    def export(self, request):
        
        id_provinsi = request.data.get('id_provinsi')
        id_kabupaten = request.data.get('id_kabupaten')
        tahun = request.data.get('tahun')
        type = request.data.get('type')
        
        try:
            if id_provinsi and id_provinsi != 0:
                data = models.DesaAllRawan.objects.filter(provinsi=id_provinsi)
                tipe_nama = models.Provinsi.objects.get(pk=id_provinsi).nama_provinsi
                file_nama_tipe = 'PROVINSI'
                file_nama_info = f'{file_nama_tipe} {tipe_nama}'
            elif id_kabupaten and id_kabupaten != 0:
                data = models.DesaAllRawan.objects.filter(kabupaten=id_kabupaten)
                tipe_nama = models.Kabupaten.objects.get(pk=id_kabupaten).nama_kabupaten
                file_nama_tipe = 'KABUPATEN'
                file_nama_info = tipe_nama
            
            df = pd.DataFrame.from_records(data.values())
            df.index += 1
            
            base_path = 'media/exported/desa'
            file_name = f'DATA DESA {file_nama_info} TAHUN {tahun}'
            file_extension = type
            file_path = f'{base_path}/{file_name}.{file_extension}'
            
            shutil.rmtree(base_path)
            os.makedirs(base_path, exist_ok=True)
            
            # Define tahun key
            status_key = f'status_{tahun}'
            keterangan_key = f'keterangan_{tahun}'
            
            # Rename header
            df.rename(columns={
                'nama_desa': 'Desa',
                'nama_kecamatan': 'Kecamatan',
                'nama_kabupaten' : 'Kabupaten',
                'nama_provinsi' : 'Provinsi',
                
                status_key : 'Status',
                keterangan_key : 'Keterangan'
            }, inplace=True)
            
            columns = ['Desa', 'Kecamatan', 'Kabupaten', 'Provinsi', 'Status', 'Keterangan']

            if type == 'csv':
                df.to_csv(file_path, mode='w', columns=columns, index=True, index_label='NO')
            else:
                writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
                sheet_name = f'{file_nama_info} {tahun}'
                df.to_excel(writer, index=True, index_label='NO',sheet_name=sheet_name  ,columns=columns)
                
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]

                # save the Excel file
                # worksheet.autofit()
                worksheet.set_column(0, 0, 6) # NO
                worksheet.set_column(1, 1, 28) # Desa
                worksheet.set_column(2, 2, 25) # Kecamatan
                worksheet.set_column(3, 3, 30) # Kabupaten
                worksheet.set_column(4, 4, 10) # Provinsi
                worksheet.set_column(6, 6, 25) # Keterangan
                
                writer.close()
            
            return Response({
                'status': True,
                'file' : f'/{file_path}',
                'info' : {
                    'detail' : {
                        'id' : id_provinsi if file_nama_tipe == 'PROVINSI' else id_kabupaten,
                        'tipe' : file_nama_tipe,
                        'nama' : file_nama_info,
                        'file_type' : type,
                        'raw' : df,
                    },
                },
                'message': 'Export data successfully',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Export data failed',
                'error': f'{str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def import_data(self, request):
        
        tahun = request.data.get('tahun')
        tipe = request.data.get('tipe') # BNNP / BNNK
        tipe_file = request.data.get('tipe_file') # File ektensi
        file = request.FILES.get('file')
        
        if not tahun or not file:
            return Response({'error': 'Tahun dan file diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if tipe_file == 'xlsx':
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
            
            cleaned_headers = [re.sub(r'\W+', '', header) for header in df.columns]

            is_valid_headers = cleaned_headers == ["NO", "Desa", "Kecamatan", "Kabupaten", "Provinsi", "Status", "Keterangan"]

            if not is_valid_headers:
                return Response({'status': False, 'message': 'Format file tidak sesuai', 'code' : 'INVALID_FORMAT'}, status=status.HTTP_400_BAD_REQUEST)
            
            kecamatan_nama = ''
            kabupaten_nama = ''
            provinsi_nama = ''
            
            for index, row in df.iterrows():
                desa_nama = row['Desa']
                desa_status = row['Status']
                kecamatan_nama = row['Kecamatan']
                kabupaten_nama = row['Kabupaten']
                provinsi_nama = row['Provinsi']

                desa = models.DBDesa.objects.filter(nama_desa=desa_nama, nama_kecamatan=kecamatan_nama).first()

                if desa:
                    kawasan_rawan, created = models.KawasanRawan.objects.get_or_create(desa=desa, tahun=tahun)
                    kawasan_rawan.status = desa_status.upper()
                    kawasan_rawan.created_by = self.request.user
                    kawasan_rawan.save()
            
            if tipe == 'bnnp':
                imported_data_wilayah_info = f'{provinsi_nama}'
            else:
                imported_data_wilayah_info = f'{kabupaten_nama} PROVINSI {provinsi_nama}'
            
            return Response({
                'status': True,
                'message': 'Data berhasil diimport',
                'info': {
                    'total': len(df),
                    'tipe' : imported_data_wilayah_info
                },
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Import data failed',
                'error': f'{str(e)}',
                'file_extension':  tipe_file
            }, status=status.HTTP_400_BAD_REQUEST)

# ======= Klasifikasi Total Kawasan Rawan Se-INDONESIA Per-Tahun =======
class TotalKawasanRawanViewSet(viewsets.ModelViewSet):
    queryset = models.TotalKawasanKawan.objects.all()
    serializer_class = serializers.TotalKawasanKawanSerializer
    filter_backends = [DjangoFilterBackend]

# =============================================
# DATABASE AWAL - DATA WILAYAH
# =============================================
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = models.Provinsi.objects.all()
    serializer_class = serializers.ProvinceSerializer
    pagination_class = pagination.Page10NumberPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = filters.ProvinceFilter
    
    @action(detail=True)
    def map_provinsi(self, request, pk):
        collection = []
        provinsi = models.ProvinsiAllRawan.objects.filter(provinsi_id=pk)
        file_path = os.path.join(os.getcwd(), f"static/geos/propinsi/{pk}.geojson")
        
        properties = {'provinsi': provinsi.nama_provinsi, 'kd_prov': pk, "total_desa": provinsi.total_desa}
        
        try:
            with open(file_path) as fl:
                data = json.load(fl)
                
                ft = geojson.Feature(geometry=data)
                collection.append(ft)
        except Exception as e:
            return Response({
                'message': 'Terjadi kesalahan saat mengambil data geojson',
                'error': 'gagal',
                'file_path': file_path
            })
            
        geo_collection = geojson.FeatureCollection(collection)
        retval = geojson.dumps(geo_collection)
        
        return Response(json.loads(retval))
        
class RegencyViewSet(viewsets.ModelViewSet):
    queryset = models.Kabupaten.objects.all()
    serializer_class = serializers.RegencySerializer
    pagination_class = pagination.Page10NumberPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['provinsi',]

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.Kecamatan.objects.all()
    serializer_class = serializers.DistrictSerializer
    pagination_class = pagination.Page10NumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = filters.DistrictFilter

class VillageViewSet(viewsets.ModelViewSet):
    queryset = models.Desa.objects.all()
    serializer_class = serializers.VillageSerializer
    pagination_class = pagination.Page10NumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.VillageFilter