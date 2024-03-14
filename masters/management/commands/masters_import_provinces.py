from csv import DictReader
from django.core.management import BaseCommand

from masters.models import reg_provinces

ALREADY_LOADED_ERROR_MESSAGE = """ Terjadi kesalahan, tabel reg_provinces sudah ada di database """

class Command(BaseCommand):
    help = "Load data provinsi dari reg_provinces.csv"

    def handle(self, *args, **options):
    
        if reg_provinces.objects.exists():
            self.stdout.write(self.style.ERROR('Data provinsi sudah ada...exiting'))
            self.stdout.write(self.style.ERROR(ALREADY_LOADED_ERROR_MESSAGE))
            return
            
        self.stdout.write('Load data provinsi ...')

        for row in DictReader(open('masters/management/data/reg_provinces.csv')):
            item=reg_provinces(
                id=row['kode_provinsi'],
                kode_provinsi=row['kode_provinsi'],
                nama_provinsi=row['nama_provinsi'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude'])
            )
            item.save()
        
        self.stdout.write(self.style.SUCCESS('Data provinsi berhasil diimport'))
        