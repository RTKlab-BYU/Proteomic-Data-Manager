# Generated by Django 3.2.7 on 2021-11-10 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0048_auto_20211108_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawfile',
            name='file_size',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='evidence_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/10'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='other_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/10'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='peptide_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/10'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='protein_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2021/11/10'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='setting_xml',
            field=models.FileField(blank=True, null=True, upload_to='maxquant_xml/2021/11/10'),
        ),
        migrations.AlterField(
            model_name='notefile',
            name='notefile',
            field=models.FileField(blank=True, null=True, upload_to='notefiles/2021/         11/10'),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='note_file',
            field=models.ManyToManyField(blank=True, to='file_manager.NoteFile'),
        ),
        migrations.AlterField(
            model_name='spectrominequeue',
            name='result_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/spectromine/2021/11/10'),
        ),
    ]