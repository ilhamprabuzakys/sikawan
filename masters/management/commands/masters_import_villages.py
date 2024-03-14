from csv import DictReader
from django.core.management import BaseCommand

from masters.models import reg_villages, reg_district

ALREADY_LOADED_ERROR_MESSAGE = """ Terjadi kesalahan, tabel reg_villages sudah ada di database """

class Command(BaseCommand):
    help = "Load data desa dari reg_villages.csv"

    def handle(self, *args, **options):
    
        if reg_villages.objects.exists():
            self.stdout.write(self.style.ERROR('Data desa sudah ada...exiting'))
            self.stdout.write(self.style.ERROR(ALREADY_LOADED_ERROR_MESSAGE))
            return
            
        self.stdout.write('Load data desa ...')

        for row in DictReader(open('masters/management/data/reg_villages.csv')):
            kode_kecamatan_id = row['kode_kecamatan_id']
            kecamatan = reg_district.objects.get(kode_kecamatan=kode_kecamatan_id)
            item=reg_villages(
                id=row['kode_desa'],
                kode_desa=row['kode_desa'],
                kode_kecamatan=kecamatan,
                nama_desa=row['nama_desa'],
                # latitude=float(row['latitude']),
                # longitude=float(row['longitude'])
            )
            item.save()
        
        self.stdout.write(self.style.SUCCESS('Data desa berhasil diimport'))