# Generated by Django 4.1 on 2023-02-04 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "app_djaagou_scan",
            "0033_rename_name_reseau_social_entreprise_social_media_name",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="all_social_media",
            old_name="name_reseau_social",
            new_name="name",
        ),
    ]
