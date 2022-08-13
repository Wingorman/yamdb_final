import os
from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews import models
from users.models import User

if settings.STATICFILES_DIRS:
    DIR_CSV = settings.STATICFILES_DIRS[0] + "data/"
else:
    DIR_CSV = settings.STATIC_ROOT + "/data/"
IMPORTS_CSV = [
    {'file': 'category.csv', 'model': models.Category,
     'inst_fields': [], 'add': False
     },
    {'file': 'genre.csv', 'model': models.Genre,
     'inst_fields': [], 'add': False
     },
    {'file': 'titles.csv', 'model': models.Title,
     'inst_fields': [
         {'field': 'category', 'csv_row': 'category',
          'model': models.Category}, ],
     'add': False
     },
    {'file': 'users.csv', 'model': User,
     'inst_fields': [], 'add': False
     },
    {'file': 'review.csv', 'model': models.Review,
     'inst_fields': [
         {'field': 'title', 'csv_row': 'title_id', 'model': models.Title},
         {'field': 'author', 'csv_row': 'author', 'model': User}, ],
     'add': False
     },
    {'file': 'comments.csv', 'model': models.Comment,
     'inst_fields': [
         {'field': 'review', 'csv_row': 'review_id', 'model': models.Review},
         {'field': 'author', 'csv_row': 'author', 'model': User}, ],
     'add': False
     },
    {'file': 'genre_title.csv', 'model': models.Title,
     'inst_fields': [],
     'add': True,
     'm2m_field_parent': 'title_id',
     'm2m_field_child':
         {'field': 'genre', 'csv_row': 'genre_id', 'model': models.Genre},
     },
]


def write_to_model(row, model, inst_fields):
    if inst_fields:
        for field in inst_fields:
            temp = field['model'].objects.get(id=row.pop(field['csv_row']))
            row[field['field']] = temp
    new = model(**row)
    new.save()


def write_m2m_model(row, model, parent, child):
    parent_inst = model.objects.get(id=row[parent])
    temp = child['model'].objects.get(id=row.pop(child['csv_row']))
    getattr(parent_inst, child['field']).add(temp)


class Command(BaseCommand):
    help = u'Наполнение базы данных из csv файлов'

    def handle(self, *args, **options):
        for in_csv in IMPORTS_CSV:
            file = in_csv['file']
            model = in_csv['model']

            if os.path.exists(DIR_CSV + file):
                if model.objects.exists() and not in_csv['add']:
                    print(f'данные в таблице {model.__name__} уже существуют! '
                          f'Вставить записи можно только в пустую таблицу.')
                    continue

                with open(DIR_CSV + file, encoding='utf-8') as csvfile:
                    reader = DictReader(csvfile, delimiter=",")
                    count = 0
                    for row in reader:
                        try:
                            if in_csv['add']:
                                write_m2m_model(
                                    row, model,
                                    in_csv['m2m_field_parent'],
                                    in_csv['m2m_field_child'])
                            else:
                                write_to_model(row, model,
                                               in_csv['inst_fields'])
                            count += 1
                        except Exception as error:
                            print(error)
                    self.stdout.write(f'в таблицу {model.__name__} вставлено '
                                      f'{count} записей')
