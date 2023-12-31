# Generated by Django 4.1 on 2023-02-07 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_djaagou_scan", "0037_alter_entreprise_social_media_phone_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Option_commande",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_menu", models.IntegerField(default=None)),
                ("id_entreprise", models.IntegerField(default=None)),
                ("quantité", models.IntegerField(default=None)),
                ("date_transaction", models.DateTimeField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name="Option_commande_intermediaire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_unknown_user", models.IntegerField(default=None)),
                ("id_menu", models.IntegerField(default=None)),
                ("id_entreprise", models.IntegerField(default=None)),
                ("quantité", models.IntegerField(default=None)),
                ("date_transaction", models.DateTimeField(default=None)),
            ],
        ),
    ]
