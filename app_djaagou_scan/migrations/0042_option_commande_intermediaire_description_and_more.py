# Generated by Django 4.1 on 2023-02-08 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "app_djaagou_scan",
            "0041_alter_option_commande_intermediaire_id_unknown_user",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="option_commande_intermediaire",
            name="description",
            field=models.CharField(default=None, max_length=65),
        ),
        migrations.AddField(
            model_name="option_commande_intermediaire",
            name="image_path",
            field=models.CharField(default=None, max_length=255),
        ),
    ]