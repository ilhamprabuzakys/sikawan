from csv import DictReader
from django.core.management import BaseCommand

from masters.models import reg_district, reg_regencies

ALREADY_LOADED_ERROR_MESSAGE = """ Terjadi kesalahan, tabel reg_districts sudah ada di database """

class Command(BaseCommand):
    help = "Load data kecamatan dari reg_districts.csv"

    def handle(self, *args, **options):
    
        if reg_district.objects.exists():
            self.stdout.write(self.style.ERROR('Data kecamatan sudah ada...exiting'))
            self.stdout.write(self.style.ERROR(ALREADY_LOADED_ERROR_MESSAGE))
            return
            
        self.stdout.write('Load data kecamatan ...')

        for row in DictReader(open('masters/management/data/reg_districts.csv')):
            kode_kabupaten_id = row['kode_kabupaten_id']
            kabupaten = reg_regencies.objects.get(kode_kabupaten=kode_kabupaten_id)
            item=reg_district(
                id=row['kode_kecamatan'],
                kode_kecamatan=row['kode_kecamatan'],
                kode_kabupaten=kabupaten,
                nama_kecamatan=row['nama_kecamatan'],
                # latitude=float(row['latitude']),
                # longitude=float(row['longitude'])
            )
            item.save()
        
        self.stdout.write(self.style.SUCCESS('Data kecamatan berhasil diimport'))