# Generated by Django 3.2.7 on 2021-09-27 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0002_auto_20210927_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawfile',
            name='name',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='project_name',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
