# Generated by Django 4.2.1 on 2023-06-19 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricefilter',
            name='price_range',
            field=models.CharField(choices=[('10000 TO 20000', '10000 TO 20000'), ('20000 TO 30000', '20000 TO 30000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000'), ('50000 and above', '50000 and above')], max_length=60),
        ),
    ]
