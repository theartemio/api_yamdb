# Generated by Django 3.2 on 2024-10-15 09:54

import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20241014_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='Год выпуска произведения.', validators=[reviews.validators.validate_year], verbose_name='Год'),
        ),
    ]
