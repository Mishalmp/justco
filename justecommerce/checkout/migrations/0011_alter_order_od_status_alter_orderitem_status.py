# Generated by Django 4.2.3 on 2023-08-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_alter_order_od_status_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Return', 'Return'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Return', 'Return'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]