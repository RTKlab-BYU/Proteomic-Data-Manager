# Generated by Django 3.2.7 on 2021-10-04 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0005_rawfile_msgfqc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawfile',
            name='rawfile',
            field=models.FileField(null=True, upload_to='rawfiles/{todays_date.year}/{todays_date.month}'),
        ),
    ]