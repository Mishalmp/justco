# Generated by Django 4.2.1 on 2023-07-19 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PriceFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_range', models.CharField(choices=[('10000 TO 20000', '10000 TO 20000'), ('20000 TO 30000', '20000 TO 30000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000'), ('50000 and above', '50000 and above')], max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_price', models.IntegerField()),
                ('product_image', models.ImageField(default='No image available', upload_to='photos/product')),
                ('product_image2', models.ImageField(default='No image available', upload_to='photos/product')),
                ('product_image3', models.ImageField(default='No image available', upload_to='photos/product')),
                ('product_description', models.TextField(blank=True)),
                ('is_available', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('quantity', models.IntegerField(default=10)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('price_range', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.pricefilter')),
            ],
        ),
        migrations.CreateModel(
            name='Variations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('image1', models.ImageField(upload_to='photos/variations')),
                ('image2', models.ImageField(upload_to='photos/variations')),
                ('image3', models.ImageField(upload_to='photos/variations')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
