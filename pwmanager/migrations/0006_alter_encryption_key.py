# Generated by Django 4.1.6 on 2023-02-12 14:59

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ("pwmanager", "0005_alter_encryption_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encryption",
            name="Key",
            field=encrypted_model_fields.fields.EncryptedCharField(
                default=b"gfYtRv4hJ4A075QeWO_1EX86-_n71pRNQPc0qe404fc="
            ),
        ),
    ]
