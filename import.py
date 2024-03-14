import os
import csv
from pathlib import Path
import sys
import django
from termcolor import colored, cprint

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from masters.models import DBDesa, KawasanRawan

"""
    Jika terjadi kesalahan dalam skrip ini, outputan hasil dari yang gagal akan disimpan pada path static/failed/
"""

separator = '-----'
csv_delimiter = ';'

def get_hasil_keseluruhan(processed_count, line_count, duplicate_entry, duplicate_count):
    print('==HASIL KESELURUHAN==')
    print('\nProcessed \t:', colored(processed_count, 'green' if processed_count > 0 else 'red'))
    print('Total CSV Line \t:', colored(line_count, 'white', attrs=['bold']))
    print('Duplicate Entry :', colored(duplicate_entry, 'green' if duplicate_entry else 'red'))
    print('Duplicate Count :', colored(duplicate_count, 'yellow'))
    print('======================')
    
def process_csv_file(file_path):
    failed_file = None
    processed_count = 0 # Jumlah row yang diproses (Desa ditemukan + Kawasan Rawan belum ada sehingga dibuat)
    line_count = 0 # Baris dari csv saat ini
    duplicate_entry = False
    duplicate_count = 0

    try:
        # Ekstrak informasi dari nama file -> 12_sumut_2023
        file_desa = Path(file_path).stem.replace('.', '')
        file_splitted_desa = file_desa.split("_")
        prov, tahun = file_splitted_desa[0], file_splitted_desa[2]
        
        failed_path = f'static/failed/failed_{prov}_{tahun}.csv'

        print(separator)
        # Open file
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
            # next(csv_reader, None)  # Skip header row
            for row in csv_reader:
                line_count += 1
                try:
                    kab, kec, desa, status = row[1].strip(), row[3].strip(), row[5].strip(), row[6].strip().upper()

                    # Cek jika ada
                    dbdesa = DBDesa.objects.filter(nama_desa__icontains=desa, nama_kecamatan__icontains=kec,
                                                provinsi__icontains=prov).filter(nama_kabupaten__icontains=kab).first()

                    if dbdesa:
                        # checked_exist_desa = Desa.objects.get(id=dbdesa.pk) # Gak perlu dicek kayaknya?
                        print(f"{line_count}: Desa {colored('ditemukan', 'green')} : Desa {dbdesa}")
                        if not KawasanRawan.objects.filter(desa=dbdesa, tahun=tahun).exists():
                            kawasan = KawasanRawan(desa=dbdesa, tahun=tahun, status=status)
                            kawasan.save()
                            processed_count += 1
                            print(f"{line_count}: {colored('Sukses', 'green')} diimport: {prov}, {kab}, {kec}, {desa}, {status}, {tahun}")
                            print(separator)
                        else:
                            duplicate_entry = True
                            duplicate_count += 1
                            print(f"{line_count}: Tidak ada perubahan. Desa dengan nama {colored('Desa ' + desa + ' tahun-' + tahun, attrs=['bold', 'underline'])} {colored('sudah ada', 'yellow')} di database")
                            print(separator)
                    else:
                        # Provinsi, Kabupaten, Kecamatan, Desa
                        text = f"{prov}, {'?' if not kab else kab}, {'?' if not kec else kec}, {'?' if not desa else desa}"
                        raise ValueError(f"Data desa {colored('tidak ditemukan', attrs=['bold'])} di DBDesa untuk data: {colored(text, 'yellow', attrs=['bold'])}")
                except (ValueError, ObjectDoesNotExist) as e:
                    # Pesan kesalahan
                    print(f"{line_count}: {colored('Error', 'red')} processing row: {row}. \nKarena: {e}")
                    print(separator)
                    if not failed_file:
                        failed_file = open(f'{failed_path}', 'w+', newline='')
                    failed_file.write(';'.join(row) + '\n')
                
            if failed_file:
                print(f"File Error disimpan di : {colored(failed_path, 'red', attrs=['underline'])}")
                print(separator)

    except Exception as e:
        print(f"Terjadi error tidak diketahui: {e}")
    finally:
        if failed_file:
            failed_file.close()

    return processed_count, line_count, duplicate_entry, duplicate_count

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Penggunaan: python manage.py process_csv_data <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    processed_count, line_count, duplicate_entry, duplicate_count = process_csv_file(file_path)
    
    get_hasil_keseluruhan(processed_count, line_count, duplicate_entry, duplicate_count)
    
    if processed_count < 1 and not duplicate_entry:
        print(f"\n{colored('ERROR!', 'red', attrs=['bold'])} Proses import gagal, {processed_count} row ter-import.\n")
    elif processed_count < 1 and duplicate_entry:
        print(f"\n{colored('WARNING!', 'yellow')} Proses import tidak berhasil, dikarenakan terdapat beberapa data yang duplikat {colored(duplicate_count, 'yellow', attrs=['bold'])} row dan {colored('0', 'red', attrs=['bold'])} row yang berhasil ter-import.\n")
    elif processed_count > 1 and duplicate_entry:
        print(f"\n{colored('WARNING!', 'yellow')} Proses import sebagian berhasil dan sebagian tidak, dikarenakan terdapat beberapa entry yang duplikat {colored(duplicate_count, 'yellow', attrs=['bold'])} row dan {colored(processed_count, 'white', attrs=['bold'])} yang berhasil ter-import.\n")
    elif processed_count > 1:
        print(f"\n{colored('BERHASIL!', 'green')} Proses import telah berhasil dengan total {colored(processed_count, 'white', attrs=['bold'])} row.\n")