# Generated by Django 3.2.7 on 2021-10-12 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0018_auto_20211011_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawfile',
            name='notefile',
            field=models.FileField(null=True, upload_to='notefiles/2021/10/12'),
        ),
        migrations.AddField(
            model_name='rawfile',
            name='notes',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='desc',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='rawfile',
            field=models.FileField(null=True, upload_to='rawfiles/2021/10/12'),
        ),
        migrations.AlterField(
            model_name='spectrominequeue',
            name='resultfile',
            field=models.FileField(blank=True, null=True, upload_to='results/2021/10/12'),
        ),
    ]
