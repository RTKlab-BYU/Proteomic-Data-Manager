# Generated by Django 3.2.7 on 2021-10-12 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0020_auto_20211012_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spectrominequeue',
            name='creator',
        ),
    ]
