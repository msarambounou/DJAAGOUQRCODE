# Generated by Django 4.1 on 2023-02-07 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_djaagou_scan", "0038_option_commande_option_commande_intermediaire"),
    ]

    operations = [
        migrations.AddField(
            model_name="option_commande",
            name="price",
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name="option_commande_intermediaire",
            name="price",
            field=models.FloatField(default=None),
        ),
    ]