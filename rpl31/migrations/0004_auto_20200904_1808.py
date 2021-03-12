# Generated by Django 3.0.6 on 2020-09-04 12:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpl31', '0003_auto_20200903_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rplusers',
            name='mobile',
            field=models.BigIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
