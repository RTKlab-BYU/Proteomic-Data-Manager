# Generated by Django 3.2.7 on 2022-02-16 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0071_alter_rawfile_note_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawfile',
            name='note_file',
            field=models.ManyToManyField(blank=True, to='file_manager.NoteFile'),
        ),
    ]
