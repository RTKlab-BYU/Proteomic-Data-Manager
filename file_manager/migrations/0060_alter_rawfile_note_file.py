# Generated by Django 3.2.7 on 2022-02-08 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0059_auto_20220208_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawfile',
            name='note_file',
            field=models.ManyToManyField(blank=True, to='file_manager.NoteFile'),
        ),
    ]