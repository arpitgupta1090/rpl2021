# Generated by Django 3.1.7 on 2021-03-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpl31', '0007_auto_20210309_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='rplusers',
            name='image',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='rplusers',
            name='image_data',
            field=models.BinaryField(null=True),
        ),
    ]
