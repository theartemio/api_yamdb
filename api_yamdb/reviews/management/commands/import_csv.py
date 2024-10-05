import os

from django.core.management.base import BaseCommand

from .constants import MODELS_TO_LOAD
from .utils import get_data_directory, get_file_names, upload_csv_data


class Command(BaseCommand):
    help = f"""
    Импорт данных из CSV файла в базу данных проекта.
    По умолчанию загружает файлы из директории static/data
    в соответствующие (указанные в названии файла) таблицы.

    Например:
    Файл category.csv будет загружен в таблицу Category.

    Импорт происходит в соответствии с указанным порядком:
    {MODELS_TO_LOAD}
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--app_name',
            type=str,
            help="""Позволяет указать приложение, в котором
            находятся модели.
            По умолчанию reviews.""",
        )
        parser.add_argument(
            '--dirpath',
            type=str,
            help="""Позволяет указать приложение директорию,
            в которой расположены файлы.
            Указывается относительно корневой папки проекта.
            По умолчанию: static/data""",
        )
        parser.add_argument(
            '--filenames',
            nargs='+',
            type=str,
            help="""Позволяет перечислить файлы, которые нужно
            импортировать.
            По умолчанию доступны все файлы из директории.
            """,
        )
        parser.add_argument(
            '--models',
            nargs='+',
            type=str,
            help=f"""Позволяет изменить список моделей, в которые нужно
            импортировать
            данные, или поменять порядок импорта.
            По умолчанию список и порядок: {MODELS_TO_LOAD}""",
        )

    def handle(self, *args, **options):
        app_name = options['app_name'] or 'reviews'
        dir_relative_path = options['dirpath'] or 'static/data'
        dir_abs_path = get_data_directory(dir_relative_path)
        files_in_dir = options['filenames'] or get_file_names(dir_abs_path)
        models = options['models'] or MODELS_TO_LOAD
        successfull_imports = []
        for model_name in models:
            related_file_name = model_name + '.csv'
            if related_file_name not in files_in_dir:
                self.stderr.write(self.style.ERROR(f"""Не найден файл
                '{related_file_name}' для модели {model_name}."""))
                answer = input("""Вы хотите ввести название файла вручную?
                При ответе 'n' импорт продолжится
                со следующей модели (y/n): """).strip().lower()
                if answer == 'y':
                    new_file_name = input(f"""Введите имя файла,
                    соответствующее модели {model_name}: """).strip()
                    related_file_name = new_file_name
                else:
                    self.stdout.write("""Импорт будет продолжен
                    со следующей модели.""")
                    continue
            path_to_file = os.path.join(dir_abs_path, related_file_name)
            try:
                upload_csv_data(path_to_file, app_name, model_name)
                successfull_imports.append(model_name)
            except Exception as error:
                self.stderr.write(self.style.ERROR(f'Ошибка! {error}'))
        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))
        if successfull_imports:
            self.stdout.write(self.style.SUCCESS(f"""Данные успешно
                                                 импортированы в модели:
                                                 {successfull_imports}."""))
