# Generated by Django 4.1 on 2023-02-04 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_djaagou_scan", "0029_user_custom_flyer_user_flyer_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="entreprise",
            old_name="nom_categorie_ets",
            new_name="secteur",
        ),
    ]
