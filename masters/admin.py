#from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from . import models

"""class KecamatanFilter(AutocompleteFilter):
    title = 'Kecamatan'
    field_name = 'kecamatan'

class KabupatenFilter(AutocompleteFilter):
    title = 'Kabupaten'
    field_name = 'kecamatan__kabupaten'

class ProvinsiFilter(AutocompleteFilter):
    title = 'Provinsi'
    field_name = 'kecamatan__kabupaten__kode_provinsi'

class RegProvincesAdmin(admin.ModelAdmin):
    search_fields = ['nama_provinsi']

admin.site.register(models.Provinsi, RegProvincesAdmin)

class RegRegenciesAdmin(admin.ModelAdmin):
    search_fields = ['nama_kabupaten']

admin.site.register(models.Kabupaten, RegRegenciesAdmin)

class RegDistrictAdmin(admin.ModelAdmin):
    search_fields = ['nama_kecamatan']

admin.site.register(models.Kecamatan, RegDistrictAdmin)

class RegVillagesAdmin(admin.ModelAdmin):
    search_fields = ['desa', 'nama_desa', 'kecamatan__nama_kecamatan', 'kecamatan__kabupaten__nama_kabupaten', 'kecamatan__kabupaten__kode_provinsi__nama_provinsi']
    list_filter = (KecamatanFilter,)

admin.site.register(models.Desa, RegVillagesAdmin)

class KawasanRawanAdmin(admin.ModelAdmin):
    search_fields = ['tahun']
    exclude = ['created_by', 'updated_by']

admin.site.register(models.KawasanRawan, KawasanRawanAdmin)"""