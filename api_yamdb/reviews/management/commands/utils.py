import csv
import os

from django.apps import apps
from django.conf import settings
from django.db import models

from .constants import MTM_MODELS


def get_file_names(directory):
    """Возвращает список имен файлов в директории."""
    return [f for f in os.listdir(directory)]


def get_data_directory(dir_relative_path):
    """Возвращает абсолютный путь в директорию с файлами."""
    data_dir = os.path.join(settings.BASE_DIR, dir_relative_path)
    return data_dir


def upload_csv_data(path_to_file, app_name, model_name):
    """Загружает данные из .csv в модель."""
    current_model = apps.get_model(app_name, model_name)
    to_create = []
    with open(path_to_file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            for field_name, field_value in line.items():
                field = current_model._meta.get_field(field_name)
                if model_name not in MTM_MODELS and isinstance(field,
                                                               models.
                                                               ForeignKey):
                    related_model = field.remote_field.model
                    related_instance = (related_model.
                                        objects.get(id=field_value))
                    line[field_name] = related_instance
            to_create.append(current_model(**line))
        current_model.objects.bulk_create(to_create)
