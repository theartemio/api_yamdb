# Generated by Django 3.2 on 2024-10-07 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
    ]
