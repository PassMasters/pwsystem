# Generated by Django 4.1.6 on 2023-02-09 15:41

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ("password", "0007_alter_encryption_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encryption",
            name="Key",
            field=encrypted_model_fields.fields.EncryptedCharField(
                default=b"Ztn_YvXMTRil2ls25uLdmCExEXTVOhggwS_dqpquPVk=", editable=False
            ),
        ),
        migrations.AlterField(
            model_name="password",
            name="TOTP",
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True),
        ),
    ]
