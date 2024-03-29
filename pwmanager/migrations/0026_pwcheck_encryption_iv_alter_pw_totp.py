# Generated by Django 4.2.4 on 2023-09-02 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('pwmanager', '0025_alter_pw_totp'),
    ]

    operations = [
        migrations.CreateModel(
            name='PWcheck',
            fields=[
                ('Owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Owner_ID', models.BigIntegerField(blank=True, default=82452355)),
                ('Test_PW', models.CharField(blank=True, max_length=500)),
                ('Answer', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='encryption',
            name='IV',
            field=models.CharField(default='0', max_length=500),
        ),
        migrations.AlterField(
            model_name='pw',
            name='TOTP',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
