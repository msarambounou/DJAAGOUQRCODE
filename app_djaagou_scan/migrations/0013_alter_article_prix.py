# Generated by Django 4.1 on 2022-12-31 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "app_djaagou_scan",
            "0012_rename_path_model_user_qrcode_path_qrcode_design_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="prix",
            field=models.IntegerField(max_length=4),
        ),
    ]