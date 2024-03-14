import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# your imports, e.g. Django models
from models import DBDesa


"""with open('../static/aceh_2023.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
        line_count += 1
    print(f'Processed {line_count} lines.')
"""
