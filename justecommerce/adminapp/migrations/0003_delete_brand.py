# Generated by Django 4.2.1 on 2023-06-19 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_brand'),
        ('adminapp', '0002_remove_brand_brand_address'),
    ]

    operations = [
        migrations.DeleteModel(
            name='brand',
        ),
    ]