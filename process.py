import os
import csv
import glob
from pathlib import Path
import psycopg2
import shutil
import sys


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
# your imports, e.g. Django models
from masters.models import DBDesa, Desa, KawasanRawan
f = sys.argv[1]
#--files = glob.glob('./static/*.csv')
#for f in files:
desa = Path(f).stem.replace('.','')
ds = desa.split("_")
prov = ds[0]
tahun = ds[2]
print("%s %s",[prov,tahun])
temp_file = 'failed_' + prov + '_'+ tahun +'.csv'
failed_file = open(temp_file,mode="w+")
with open(f) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        print(row)
        kab = row[0].strip()
        kec = row[2].strip()
        desa = row[5].strip()
        status = row[6].strip().upper()
        dbdesa = DBDesa.objects.filter(nama_desa__icontains = desa,nama_kecamatan__icontains = kec, provinsi__icontains = prov).filter(nama_kabupaten__icontains=kab)
        if dbdesa:
            ddesa = Desa.objects.get(id = dbdesa[0].desa)
            print([prov, kab,kec, desa, dbdesa[0].desa, status, tahun])
            kawasan = KawasanRawan(desa=dbdesa[0], tahun=tahun, status = status)
            kawasan.save()
        else:
            failed_file.write(";".join(row) + "\n")

        #break
    print('Selesai')
