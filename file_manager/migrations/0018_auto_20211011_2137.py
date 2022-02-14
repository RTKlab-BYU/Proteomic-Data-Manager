# Generated by Django 3.2.7 on 2021-10-12 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0017_auto_20211012_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawfile',
            name='rawfile',
            field=models.FileField(null=True, upload_to='rawfiles/2021/10/11'),
        ),
        migrations.AlterField(
            model_name='spectrominequeue',
            name='resultfile',
            field=models.FileField(blank=True, null=True, upload_to='results/2021/10/11'),
        ),
    ]
