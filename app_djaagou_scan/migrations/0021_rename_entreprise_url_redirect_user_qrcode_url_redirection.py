# Generated by Django 4.1 on 2023-01-03 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "app_djaagou_scan",
            "0020_rename_url_redirect_user_qrcode_entreprise_url_redirect",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="user_qrcode",
            old_name="entreprise_url_redirect",
            new_name="url_redirection",
        ),
    ]
