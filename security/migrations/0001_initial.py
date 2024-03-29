# Generated by Django 4.2.4 on 2023-11-19 20:20

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
            name='Device',
            fields=[
                ('Name', models.CharField(max_length=255)),
                ('Pub_key', models.CharField(max_length=1024)),
                ('UID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserServerKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='1', max_length=1024)),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='keytransfer',
            fields=[
                ('UID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security.device')),
                ('Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
