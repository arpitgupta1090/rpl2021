# Generated by Django 3.1.7 on 2021-03-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpl31', '0006_auto_20201003_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selected',
            name='point',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
    ]
