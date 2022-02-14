# Generated by Django 3.2.7 on 2021-10-05 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0009_auto_20211004_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpectromineQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runstatus', models.BooleanField(default=False, null=True)),
                ('ProteinID', models.IntegerField(blank=True, null=True)),
                ('PeptideID', models.IntegerField(blank=True, null=True)),
                ('starttime', models.DateTimeField(blank=True, null=True)),
                ('finishedtime', models.DateTimeField(blank=True, null=True)),
                ('creator', models.TextField(blank=True, max_length=100, null=True)),
                ('resultfile', models.FileField(null=True, upload_to='results/2021/10')),
                ('Rawfile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='file_manager.rawfile')),
            ],
        ),
    ]
