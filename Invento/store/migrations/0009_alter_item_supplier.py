# Generated by Django 5.1.2 on 2024-10-17 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_alter_item_supplier_alter_supplier_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="supplier",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.supplier",
            ),
        ),
    ]
