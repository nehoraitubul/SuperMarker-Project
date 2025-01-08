# Generated by Django 4.1.7 on 2023-05-09 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0032_cart_products_alter_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit_of_measure_price',
            field=models.DecimalField(db_column='unit_of_measure_price', decimal_places=2, max_digits=10),
        ),
    ]