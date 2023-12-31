# Generated by Django 4.1 on 2022-12-10 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_djaagou_scan", "0002_delete_social_media_link"),
    ]

    operations = [
        migrations.CreateModel(
            name="social_media_link",
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
                ("image_path", models.CharField(default=None, max_length=255)),
                ("name_reseau_social", models.CharField(max_length=25)),
                ("id_user", models.IntegerField(default=None)),
            ],
        ),
    ]
