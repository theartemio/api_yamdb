# Generated by Django 3.2 on 2024-10-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.SmallIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
