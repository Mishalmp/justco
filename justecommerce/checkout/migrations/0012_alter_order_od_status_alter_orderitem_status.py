# Generated by Django 4.2.1 on 2023-07-11 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_alter_order_od_status_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Return', 'Return'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Return', 'Return'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]
