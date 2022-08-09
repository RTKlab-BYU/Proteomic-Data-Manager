# Generated by Django 3.2.7 on 2021-11-09 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0047_auto_20211108_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maxquantqueue',
            name='evidence_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/8'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='other_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/8'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='peptide_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/8'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='protein_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/8'),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='note_file',
            field=models.ManyToManyField(blank=True, to='file_manager.NoteFile'),
        ),
        migrations.AlterField(
            model_name='spectrominequeue',
            name='result_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/spectromine/2021/11/8'),
        ),
    ]