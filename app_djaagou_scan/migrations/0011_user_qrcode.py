# Generated by Django 4.1 on 2022-12-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_djaagou_scan", "0010_abonnement"),
    ]

    operations = [
        migrations.CreateModel(
            name="user_qrcode",
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
                ("id_user", models.IntegerField(default=None)),
                ("nom_entreprise", models.CharField(max_length=40)),
                ("path_model", models.CharField(default=None, max_length=255)),
            ],
        ),
    ]
