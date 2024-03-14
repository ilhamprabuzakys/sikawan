from csv import DictReader
import csv
from pathlib import Path
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from import_export.fields import ObjectDoesNotExist
from termcolor import colored, cprint

from django.db.models import Q

from users.models import Profile, Satker, SatkerBNNK
from masters.models import Kabupaten

class Command(BaseCommand):
    help = "Generate data user BNNK"
    separator = '-----'
    
    matched_count = 0
    unmatched_count = 0
    processed_count = 0
    duplicate_entry = False
    duplicate_entry_row = []
    duplicate_count = 0
    iteration = 0
    
    def get_hasil_keseluruhan(self):
        print(f'==HASIL KESELURUHAN ==\n{self.separator}')
        print('Dibuatkan\t :', colored(self.processed_count, 'green'))
        print('Duplicate\t :', colored(self.duplicate_count, 'yellow'))
        print('======================')
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\nProses dimulai!\n'))
        
        try:
            total_bnnk_count = SatkerBNNK.objects.count()
            total_kabupaten_count = Kabupaten.objects.count()
            
            print('Total satuan kerja BNNK :', total_bnnk_count)
            print('Total Kabupaten :', total_kabupaten_count)
            
            list_satker = SatkerBNNK.objects.all()
            list_kabupaten = Kabupaten.objects.all()
            
            for satker in list_satker:
                self.iteration += 1
                
                if satker.jumlah_profil != 0:
                    print(f"{colored('EXIST :', 'yellow')} Satuan Kerja {colored(satker.nama_satker, attrs=['bold'])} sudah memiliki perwakilan user : {satker.jumlah_profil} ...")
                    self.duplicate_count += 1
                    
                    pass
                else:
                    
                    cleaned_nama_satker = satker.nama_satker.strip()
                    
                    data = {
                        'first_name': cleaned_nama_satker,
                        'username': cleaned_nama_satker.lower().replace(" ", "_"),
                        'password': cleaned_nama_satker.lower().replace(" ", "_"),
                        'is_staff': True,
                        'is_superuser': False,
                    }
                    
                    user = User.objects.create_user(**data)
                    user.set_password(data['password'])
                    user.save()
                    
                    profile = Profile.objects.create(user=user, satker_id=satker.satker_id)
                    
                    self.processed_count += 1
                    
                    user_pk_profile_pk = f'ID User : {user.pk}, ID Profile : {profile.pk}'
                    
                    print(f"{colored(self.iteration, attrs=['bold'])}: {colored('SUCCESS :', 'green')} Data user untuk Satuan Kerja {colored(user.first_name, attrs=['bold'])} berhasil dibuat ... {user_pk_profile_pk}")
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"Perwakilan untuk Satker: {satker.nama_satker}, berhasil dibuatkan !")
                    )
        except Exception as e:
            print(f"{colored(e, 'red', attrs=['bold'])}")
            self.stdout.write(self.style.ERROR(f'\nProses dihentikan karena terjadi error!\n'))
            return
        finally:
            self.get_hasil_keseluruhan()
            
            self.stdout.write(self.style.SUCCESS('\nProses telah selesai\n'))
            
            return
        
    # def add_arguments(self, parser):
    #     parser.add_argument('--prevent_duplicates', type=int, default=1, help='Prevent duplicate entry')
    #       print(f"{colored(no, attrs=['bold'])}: {colored('SUCCESS :', 'green')} Data user untuk Satuan Kerja {colored(user.first_name, attrs=['bold'])} berhasil dibuat ... {user_pk_profile_pk}")


    # data = {
                        #     'first_name': satker.nama_satker,
                        #     'username': satker.nama_satker.lower().replace(" ", "_"),
                        #     'password': satker.nama_satker.lower().replace(" ", "_"),
                        #     'is_staff': True,
                        #     'is_superuser': False,
                        # }
                        
                        # user = User.objects.create_user(**data)
                        # user.set_password(data['password'])
                        # user.save()
                        
                        # profile = Profile.objects.create(user=user, satker_id=satker.satker_id)
                        # user_pk_profile_pk = f'ID User : {user.pk}, ID Profile : {profile.pk}'
                        
                        # self.processed_count += 1

                        # print(f"{colored(no, attrs=['bold'])}: {colored('SUCCESS :', 'green')} Data user untuk Satuan Kerja {colored(user.first_name, attrs=['bold'])} berhasil dibuat ... {user_pk_profile_pk}")