# Generated by Django 5.1.2 on 2024-10-19 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_transaction"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="minimum",
            new_name="threshold",
        ),
    ]
