# Generated by Django 4.1.6 on 2023-02-09 15:39

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ("password", "0006_encryption"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encryption",
            name="Key",
            field=encrypted_model_fields.fields.EncryptedCharField(
                default=b"9nwXw6SE-bdkZi1whyndM38Mi7vMzXM7nliy76bOwJ0=", editable=False
            ),
        ),
    ]
