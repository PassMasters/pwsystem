# Generated by Django 4.1.6 on 2023-02-12 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrative", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="One_Detail",
            field=models.CharField(blank=True, max_length=280),
        ),
    ]
