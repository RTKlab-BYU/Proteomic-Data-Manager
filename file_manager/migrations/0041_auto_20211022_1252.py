# Generated by Django 3.2.7 on 2021-10-22 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0040_auto_20211022_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawfile',
            name='content_extracted',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='note_file',
            field=models.ManyToManyField(blank=True, to='file_manager.NoteFile'),
        ),
    ]
