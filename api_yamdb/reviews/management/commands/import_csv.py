from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title
import os
from django.apps import apps
from django.conf import settings
from .utils import get_file_names, get_data_directory, upload_csv_data



class Command(BaseCommand):
    help = """
    Импорт данных из CSV файла в базу данных проекта.
    По умолчанию загружает все файлы из директории static/data
    в соответствующие (указанные в названии файла) таблицы.

    Например:
    Файл category.csv будет загружен в таблицу Category.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--app_name',
            type=str,
            help="""Приложение, в котором работает модель.
            По умолчанию reviews.""",
        )
        parser.add_argument(
            '--dirpath',
            type=str,
            help="""Директория, в которой расположены файлы.
            Указывается относительно корневой папки проекта.
            Пример: static/data""",
        )
        parser.add_argument(
            '--filenames',
            nargs='+',
            type=str,
            help="""Список файлов, которые необходимо импортировать.
            Позволяет: 1) избирательно импортировать несколько файлов или
            2) импортировать один файл в конкретную модель с использованием
            аргумента --modelname, даже если их имена не совпадают.""",
        )
        parser.add_argument(
            '--model',
            type=str,
            help="""Имя модели, в которую необходимо импортировать.
            Позволяет импортировать данные в модель в случае, если
            у файла и модели не совпадают имена.
            Работает только в случае импорта одного файла.""",
        )

    def handle(self, *args, **options):
        model_app = options['app_name'] or 'reviews'
        dir_relative_path = options['dirpath'] or 'static/data'
        dir_abs_path = get_data_directory(dir_relative_path)
        file_names = options['filenames'] or get_file_names(dir_abs_path)
        successfull_imports = []
        for file_name in file_names:
            if len(file_names) == 1 and options['model']:
                model_name = options['model']
            else:
                model_name = os.path.splitext(file_name)[0]
            path_to_file = os.path.join(dir_abs_path, file_name)
            try:
                current_model = apps.get_model(model_app, model_name)
                upload_csv_data(path_to_file, current_model, model_name)
                successfull_imports.append(model_name)
            except Exception as error:
                self.stderr.write(self.style.ERROR(f'Ошибка! {error}'))
        stdout_message = f"""Импорт завершен!
        Данные успешно импортированы в модели: {successfull_imports}."""
        self.stdout.write(self.style.SUCCESS(stdout_message))
