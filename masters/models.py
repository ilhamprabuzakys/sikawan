from random import randint
from django.contrib.auth.models import User
from django.db import models

class Provinsi(models.Model):
    provinsi = models.CharField(max_length=10)
    nama_provinsi = models.CharField(max_length=100)
    provinsi_singkat = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    latitude2 = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude2 = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    geom = models.JSONField(null=True)
    line_geom = models.JSONField(null=True)
    
    class Meta:
        ordering = ['-latitude', ]
        verbose_name = 'Provinsi'
        verbose_name_plural = 'Daftar Provinsi'
        db_table = 'masters_data_provinsi'
        
    def get_kawasan_count(self):
        return randint(100, 900)
    
    def __str__(self):
        return f'{self.nama_provinsi.capitalize()}'

class Kabupaten(models.Model):
    kabupaten = models.CharField(max_length=10)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE, null=True, blank=True)
    nama_kabupaten = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    geom = models.JSONField(null=True)

    class Meta:
        # ordering = ['nama_kabupaten', ]
        verbose_name = 'Kabupaten'
        verbose_name_plural = 'Daftar Kabupaten'
        db_table = 'masters_data_kabupaten'
        
    def __str__(self):
        return str(self.nama_kabupaten)

class Kecamatan(models.Model):
    kecamatan = models.CharField(max_length=10)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, null=True, blank=True)
    nama_kecamatan = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    geom = models.JSONField(null=True)

    class Meta:
        # ordering = ['nama_kecamatan', ]
        verbose_name = 'Kecamatan'
        verbose_name_plural = 'Daftar Kecamatan'
        db_table = 'masters_data_kecamatan'

    def __str__(self):
        return str(self.nama_kecamatan)

class Desa(models.Model):
    desa = models.CharField(max_length=10)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE, null=True, blank=True)
    nama_desa = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    geom = models.JSONField(null=True)

    def get_kawan(self, tahun):
        kawan = self.kawasan_rawan.filter(tahun=tahun).first()
        if kawan:
            return kawan
        return None
    
    def get_full_location(self, type):
        output = ''
        if type == 'nama':
            nama_kecamatan = self.kecamatan.nama_kecamatan if self.kecamatan else ""
            nama_kabupaten = self.kecamatan.kabupaten.nama_kabupaten if self.kecamatan else ""
            nama_provinsi = self.kecamatan.kabupaten.provinsi.nama_provinsi if self.kecamatan else ""
            output = f'{self.nama_desa}, {nama_kecamatan}, {nama_kabupaten}, {nama_provinsi}'
        else:
            kecamatan = self.kecamatan.kecamatan if self.kecamatan else ""
            kabupaten = self.kecamatan.kabupaten.kabupaten if self.kecamatan else ""
            provinsi = self.kecamatan.kabupaten.provinsi.provinsi if self.kecamatan else ""
            output = f'{self.desa}, {kecamatan}, {kabupaten}, {provinsi}'
            
        return output
    
    class Meta:
        ordering = ['-updated_at', ]
        verbose_name = 'Desa'
        verbose_name_plural = 'Daftar Desa'
        db_table = 'masters_data_desa'
    
    def __str__(self):
        output = f'{self.desa} Desa {self.nama_desa}'
        return output

# Untuk select2
class DesaView(models.Model):
    desa_lengkap = models.TextField(null=True)
    desa = models.CharField(max_length=100, null=True)
    kecamatan = models.CharField(max_length=100, null=True)
    propinsi = models.CharField(max_length=100, null=True)
    desa_id = models.ForeignKey(Desa, on_delete=models.DO_NOTHING, null=True, related_name='desa_view')
    
    class Meta:
        managed = False
        db_table = 'masters_view_desa'
        
    def __str__(self):
        return str(self.desa_lengkap)

class DBDesa(models.Model):
    desa = models.CharField(max_length=10,null=True)
    kecamatan = models.CharField(max_length=10, null=True)
    kabupaten = models.CharField(max_length=10, null=True)
    provinsi = models.CharField(max_length=10, null=True)
    nama_desa = models.CharField(max_length=100, null=True)
    nama_kecamatan = models.CharField(max_length=100, null=True)
    nama_kabupaten = models.CharField(max_length=100, null=True)
    nama_provinsi = models.CharField(max_length=100, null=True)
    
    class Meta:
        managed = False
        db_table = 'masters_db_desa'
        
    def __str__(self):
        desa_lengkap = f'{self.nama_desa}, {self.nama_kecamatan}, {self.nama_kabupaten}, {self.nama_provinsi}'
        return desa_lengkap

class ProvinsiRawan(models.Model):
    provinsi = models.CharField(max_length=10, null=True)
    nama_provinsi = models.CharField(max_length=100, null=True)
    siaga = models.IntegerField()
    bahaya = models.IntegerField()
    waspada = models.IntegerField()
    aman = models.IntegerField()
    tahun = models.CharField(max_length=4)
    
    class Meta:
        managed = False
        db_table = 'masters_provinsi_rawan'

class ProvinsiRawanGeom(models.Model):
    #provinsi = models.CharField(max_length=10, null=True)
    #nama_provinsi = models.CharField(max_length=100, null=True)
    geom = models.CharField(max_length=300)
    tahun = models.CharField(max_length=4)
    
    class Meta:
        managed = False
        db_table = 'masters_provinsi_rawan_geom'

class KawasanRawan(models.Model):
    STATUS_CHOICES = (
        ("BAHAYA", "BAHAYA"),
        ("WASPADA", "WASPADA"),
        ("SIAGA", "SIAGA"),
        ("AMAN", "AMAN"),
        ("KOSONG", "KOSONG"),
    )
    
    TAHUN_CHOICES = (
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
        ("2024", "2024"),
    )
    
    desa = models.ForeignKey(DBDesa, on_delete=models.CASCADE, null=True, blank=True, related_name="kawasan_rawan")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True, blank=True)
    tahun = models.CharField(max_length=4, choices=TAHUN_CHOICES, null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="kawan_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="kawan_updated_by")

    class Meta:
        verbose_name = 'Kawasan Rawan'
        verbose_name_plural = 'Daftar Kawasan Rawan'
        db_table = 'masters_kawasan_rawan'
        ordering = ['updated_at']
    
# Untuk keperluan kalkulasi data dari semua tahun dan dapatkan jumlah kawasan_rawan per-desanya
# Performa sudah lumayan optimal total fetch time : 0.35s
class ProvinsiAllRawan(models.Model):
    provinsi_id = models.IntegerField()
    nama_provinsi = models.CharField(max_length=100, null=True)
    total_desa = models.IntegerField()
    total_2023 = models.IntegerField()
    total_2022 = models.IntegerField()
    total_2021 = models.IntegerField()
    
    bahaya_2023 = models.IntegerField()
    waspada_2023 = models.IntegerField()
    siaga_2023 = models.IntegerField()
    aman_2023 = models.IntegerField()
    
    bahaya_2022 = models.IntegerField()
    waspada_2022 = models.IntegerField()
    siaga_2022 = models.IntegerField()
    aman_2022 = models.IntegerField()
    
    bahaya_2021 = models.IntegerField()
    waspada_2021 = models.IntegerField()
    siaga_2021 = models.IntegerField()
    aman_2021 = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'masters_all_provinsi_rawan'

class KabupatenAllRawan(models.Model):
    provinsi_id = models.IntegerField()
    kabupaten_id = models.IntegerField()
    nama_provinsi = models.CharField(max_length=100, null=True)
    nama_kabupaten = models.CharField(max_length=100, null=True)
    total_desa = models.IntegerField()
    total_2023 = models.IntegerField()
    total_2022 = models.IntegerField()
    total_2021 = models.IntegerField()
    
    bahaya_2023 = models.IntegerField()
    waspada_2023 = models.IntegerField()
    siaga_2023 = models.IntegerField()
    aman_2023 = models.IntegerField()
    
    bahaya_2022 = models.IntegerField()
    waspada_2022 = models.IntegerField()
    siaga_2022 = models.IntegerField()
    aman_2022 = models.IntegerField()
    
    bahaya_2021 = models.IntegerField()
    waspada_2021 = models.IntegerField()
    siaga_2021 = models.IntegerField()
    aman_2021 = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'masters_all_kabupaten_rawan'

class KecamatanAllRawan(models.Model):
    provinsi_id = models.IntegerField()
    kabupaten_id = models.IntegerField()
    kecamatan_id = models.IntegerField()
    nama_provinsi = models.CharField(max_length=100, null=True)
    nama_kabupaten = models.CharField(max_length=100, null=True)
    nama_kecamatan = models.CharField(max_length=100, null=True)
    total_desa = models.IntegerField()
    total_2023 = models.IntegerField()
    total_2022 = models.IntegerField()
    total_2021 = models.IntegerField()
    
    bahaya_2023 = models.IntegerField()
    waspada_2023 = models.IntegerField()
    siaga_2023 = models.IntegerField()
    aman_2023 = models.IntegerField()
    
    bahaya_2022 = models.IntegerField()
    waspada_2022 = models.IntegerField()
    siaga_2022 = models.IntegerField()
    aman_2022 = models.IntegerField()
    
    bahaya_2021 = models.IntegerField()
    waspada_2021 = models.IntegerField()
    siaga_2021 = models.IntegerField()
    aman_2021 = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'masters_all_kecamatan_rawan'

class DesaAllRawan(models.Model):
    desa = models.CharField(max_length=10,null=True)
    kecamatan = models.CharField(max_length=10, null=True)
    kabupaten = models.CharField(max_length=10, null=True)
    provinsi = models.CharField(max_length=10, null=True)
    nama_desa = models.CharField(max_length=100, null=True)
    nama_kecamatan = models.CharField(max_length=100, null=True)
    nama_kabupaten = models.CharField(max_length=100, null=True)
    nama_provinsi = models.CharField(max_length=100, null=True)
    
    status_2021 = models.CharField(max_length=100, null=True)
    status_2022 = models.CharField(max_length=100, null=True)
    status_2023 = models.CharField(max_length=100, null=True)
    status_2024 = models.CharField(max_length=100, null=True)
    keterangan_2021 = models.TextField()
    keterangan_2022 = models.TextField()
    keterangan_2023 = models.TextField()
    keterangan_2024 = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'masters_all_desa_rawan'
        # db_table = 'masters_db_desa'
        
    def __str__(self):
        desa_lengkap = f'{self.nama_desa}, {self.nama_kecamatan}, {self.nama_kabupaten}, {self.nama_provinsi}'
        return desa_lengkap
        
class TotalKawasanKawan(models.Model):
    tahun = models.CharField(max_length=100, null=True)
    total = models.IntegerField()
    bahaya = models.IntegerField()
    waspada = models.IntegerField()
    siaga = models.IntegerField()
    aman = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'masters_total_kawasan_rawan_per_tahun'
        
