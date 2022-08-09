# Generated by Django 3.2.7 on 2022-01-14 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_manager', '0055_auto_20211203_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_name', models.TextField(blank=True, max_length=100, null=True)),
                ('result_file', models.FileField(blank=True, null=True, upload_to='hdstorage/proteindiscoverer/2022/1/14')),
                ('run_status', models.BooleanField(default=False, null=True)),
                ('psm_id', models.IntegerField(blank=True, null=True)),
                ('peptide_id', models.IntegerField(blank=True, null=True)),
                ('protein_id', models.IntegerField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finished_time', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='evidence_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='other_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='peptide_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='protein_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/maxquant/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='maxquantqueue',
            name='setting_xml',
            field=models.FileField(blank=True, null=True, upload_to='maxquant_xml/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='msfraggerqueue',
            name='ion_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/msfragger/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='msfraggerqueue',
            name='peptide_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/msfragger/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='msfraggerqueue',
            name='protein_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/msfragger/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='msfraggerqueue',
            name='psm_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/msfragger/2022/1/14'),
        ),
        migrations.AlterField(
            model_name='notefile',
            name='notefile',
            field=models.FileField(blank=True, null=True, upload_to='notefiles/2022/         1/14'),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='note_file',
            field=models.ManyToManyField(blank=True, to='file_manager.NoteFile'),
        ),
        migrations.AlterField(
            model_name='spectrominequeue',
            name='result_file',
            field=models.FileField(blank=True, null=True, upload_to='hdstorage/spectromine/2022/1/14'),
        ),
        migrations.CreateModel(
            name='PdWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_name', models.TextField(blank=True, max_length=100, null=True)),
                ('worker_ip', models.TextField(blank=True, max_length=100, null=True)),
                ('worker_status', models.TextField(blank=True, max_length=100, null=True)),
                ('last_update', models.DateTimeField(blank=True, null=True)),
                ('current_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='file_manager.pdqueue')),
            ],
        ),
        migrations.AddField(
            model_name='pdqueue',
            name='rawfile',
            field=models.ManyToManyField(to='file_manager.RawFile'),
        ),
    ]