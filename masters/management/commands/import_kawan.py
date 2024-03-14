from csv import DictReader
import csv
from pathlib import Path
from django.core.management import BaseCommand
from import_export.fields import ObjectDoesNotExist
from termcolor import colored, cprint

from masters.models import DBDesa, KawasanRawan

class Command(BaseCommand):
    help = "Import data Kawasan Rawan dari file CSV"
    separator = '-----'
    csv_delimiter = ';'
    # csv_delimiter = ','
    
    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path file csv')
        
        # parser.add_argument('index_kabupaten', type=int, help='Index kabupaten')
        # parser.add_argument('index_kecamatan', type=int, help='Index kecamatan')
        # parser.add_argument('index_desa', type=int, help='Index desa')
        # parser.add_argument('index_status', type=int, help='Index status')
        
    def get_hasil_keseluruhan(self, processed_count, line_count, duplicate_entry, duplicate_count, duplicate_entry_row, tahun):
        print(f'==HASIL KESELURUHAN {tahun} ==\n{self.separator}')
        print('Processed \t:', colored(processed_count, 'green' if processed_count > 0 else 'red'))
        print('Total CSV Line \t:', colored(line_count, 'white', attrs=['bold']))
        print('Duplicate Entry :', colored(duplicate_entry, 'green' if duplicate_entry else 'red'))
        print('Duplicate Row :', duplicate_entry_row)
        print('Duplicate Count :', colored(duplicate_count, 'yellow'))
        print('======================')

    def handle(self, *args, **options):
        file_path = options['path']
        
        failed_file = None
        processed_count = 0 # Jumlah row yang diproses (Desa ditemukan + Kawasan Rawan belum ada sehingga dibuat)
        line_count = 0 # Baris dari csv saat ini
        duplicate_entry = False
        duplicate_entry_row = []
        duplicate_count = 0
        selected_tahun = 0
    
        try:
            self.stdout.write(self.style.SUCCESS('\nProses dimulai!\n'))
            
            # Ekstrak informasi dari nama file -> 12_sumut_2023
            file_desa = Path(file_path).stem.replace('.', '')
            file_splitted_desa = file_desa.split("_")
            prov, tahun = file_splitted_desa[0], file_splitted_desa[2]
            selected_tahun = tahun
            
            failed_path = f'static/failed/{tahun}/failed_{prov}_{tahun}.csv'

            print(self.separator)
            # Open file
            with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.csv_delimiter)
                # next(csv_reader, None)  # Skip header row
                for row in csv_reader:
                    line_count += 1
                    try:
                        kab, kec, desa, status = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip().upper()

                        # Cek jika ada
                        dbdesa = DBDesa.objects.filter(nama_desa__icontains=desa, nama_kecamatan__icontains=kec,
                                                    provinsi__icontains=prov).filter(nama_kabupaten__icontains=kab).first()

                        if dbdesa:
                            # checked_exist_desa = Desa.objects.get(id=dbdesa.pk) # Gak perlu dicek kayaknya?
                            print(f"{line_count}: Desa {colored('ditemukan', 'green')} : Desa {dbdesa}")
                            
                            kawasan_rawan = KawasanRawan.objects.create(desa=dbdesa, tahun=tahun, status=status)
                            processed_count += 1
                            
                            print(f"{line_count}: {colored('Row Sukses', 'green')} diimport: {kawasan_rawan.pk} {row}")
                            print(self.separator)
                            
                            # kawasan, created = KawasanRawan.objects.get_or_create(desa=dbdesa, tahun=tahun, status=status)
                            # if created:
                            #     processed_count += 1
                            #     print(f"{line_count}: {colored('Row Sukses', 'green')} diimport: {row}")
                            #     # print(f"{line_count}: {colored('Sukses', 'green')} diimport: {prov}, {kab}, {kec}, {desa}, {status}, {tahun}")
                            #     print(self.separator)
                            # else:
                            #     duplicate_entry = True
                            #     duplicate_count += 1
                            #     duplicate_entry_row.append(line_count)
                            #     print(f"{line_count}: Tidak ada perubahan. Data Kawasan Rawan untuk Desa dengan ID {colored(dbdesa.desa, 'yellow')} - {colored('Desa ' + desa + ' tahun-' + tahun, attrs=['bold', 'underline'])} {colored('sudah ada', 'yellow')} di tabel {colored('masters_kawasan_rawan', attrs=['bold'])}")
                            #     print(self.separator)
                        else:
                            # Provinsi, Kabupaten, Kecamatan, Desa
                            # text = f"{prov}, {'?' if not kab else kab}, {'?' if not kec else kec}, {'?' if not desa else desa}"
                            text = f"Provinsi : {prov}, Kab : {'?' if not kab else kab}, Kec : {'?' if not kec else kec}, Desa : {'?' if not desa else desa}"
                            raise ValueError(f"Data desa {colored('tidak ditemukan', attrs=['bold'])} di DBDesa untuk data: {colored(text, 'yellow', attrs=['bold'])}")
                    except (ValueError, ObjectDoesNotExist) as e:
                        # Pesan kesalahan
                        print(f"{line_count}: {colored('Error', 'red')} processing row: {row}. \nKarena: {e}")
                        print(self.separator)
                        if not failed_file:
                            failed_file = open(f'{failed_path}', 'w+', newline='')
                        failed_file.write(';'.join(row) + '\n')
                    
                if failed_file:
                    print(f"File Error disimpan di : {colored(failed_path, 'red', attrs=['underline'])}")
                    print(self.separator)

        except Exception as e:
            print(f"Terjadi error tidak diketahui: {e}")
            return
        finally:
            if failed_file:
                failed_file.close()
            self.get_hasil_keseluruhan(processed_count, line_count, duplicate_entry, duplicate_count, duplicate_entry_row, selected_tahun)
            
            if processed_count < 1 and not duplicate_entry:
                print(f"\n{colored('ERROR!', 'red', attrs=['bold'])} Proses import gagal, {processed_count} row ter-import.")
            elif processed_count < 1 and duplicate_entry:
                print(f"\n{colored('WARNING!', 'yellow')} Proses import tidak berhasil, dikarenakan terdapat beberapa data yang duplikat {colored(duplicate_count, 'yellow', attrs=['bold'])} row dan {colored('0', 'red', attrs=['bold'])} row yang berhasil ter-import.")
            elif processed_count > 1 and duplicate_entry:
                print(f"\n{colored('WARNING!', 'yellow')} Proses import sebagian berhasil dan sebagian tidak, dikarenakan terdapat beberapa entry yang duplikat {colored(duplicate_count, 'yellow', attrs=['bold'])} row dan {colored(processed_count, 'white', attrs=['bold'])} yang berhasil ter-import.")
            elif processed_count > 1:
                print(f"\n{colored('BERHASIL!', 'green')} Proses import telah berhasil dengan total {colored(processed_count, 'white', attrs=['bold'])} row.")

        self.stdout.write(self.style.SUCCESS('\nProses telah selesai\n'))
        
# Terdapat bug di kepulauanRiau_2022