# Generated by Django 4.1 on 2023-02-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_djaagou_scan", "0046_remove_option_commande_intermediaire_numero_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="option_commande",
            name="custumer_name",
            field=models.CharField(default=None, max_length=25),
        ),
    ]