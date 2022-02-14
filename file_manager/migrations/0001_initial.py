# Generated by Django 3.2.7 on 2021-09-24 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RawFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('project_name', models.TextField(max_length=100)),
                ('desc', models.TextField(blank=True, max_length=100, null=True)),
                ('rawfile', models.FileField(upload_to='rawfiles/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holder_creater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
