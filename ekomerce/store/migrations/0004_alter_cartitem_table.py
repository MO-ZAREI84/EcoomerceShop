# Generated by Django 5.1.6 on 2025-02-19 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_quntity_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cartitem',
            table='CartItem',
        ),
    ]
