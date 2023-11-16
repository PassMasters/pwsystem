# Generated by Django 4.2.4 on 2023-11-15 01:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('security', '0002_remove_device_salt_device_pub_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='Cookie_ID',
        ),
        migrations.RemoveField(
            model_name='device',
            name='Device_UUID',
        ),
        migrations.RemoveField(
            model_name='device',
            name='id',
        ),
        migrations.AlterField(
            model_name='device',
            name='Pub_key',
            field=models.CharField(default='10000', max_length=1024, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='UserServerKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='1', max_length=1024)),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]