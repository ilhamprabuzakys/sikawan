from csv import DictReader
from django.core.management import BaseCommand

from masters.models import reg_regencies, reg_provinces

ALREADY_LOADED_ERROR_MESSAGE = """ Terjadi kesalahan, tabel reg_regencies sudah ada di database """

class Command(BaseCommand):
    help = "Load data kabupaten dari reg_regencies.csv"

    def handle(self, *args, **options):
    
        if reg_regencies.objects.exists():
            self.stdout.write(self.style.ERROR('Data kabupaten sudah ada...exiting'))
            self.stdout.write(self.style.ERROR(ALREADY_LOADED_ERROR_MESSAGE))
            return
            
        self.stdout.write('Load data kabupaten ...')

        for row in DictReader(open('masters/management/data/reg_regencies.csv')):
            kode_provinsi_id = row['kode_provinsi_id']
            provinsi = reg_provinces.objects.get(kode_provinsi=kode_provinsi_id)
            item=reg_regencies(
                id=row['kode_kabupaten'],
                kode_kabupaten=row['kode_kabupaten'],
                kode_provinsi=provinsi,
                nama_kabupaten=row['nama_kabupaten'],
                # latitude=float(row['latitude']),
                # longitude=float(row['longitude'])
            )
            item.save()
        
        self.stdout.write(self.style.SUCCESS('Data kabupaten berhasil diimport'))