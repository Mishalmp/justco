# Generated by Django 4.2.1 on 2023-07-24 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Return', 'Return'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Return', 'Return'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
    ]
