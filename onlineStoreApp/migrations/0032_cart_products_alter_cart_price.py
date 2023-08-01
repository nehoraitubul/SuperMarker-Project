# Generated by Django 4.1.7 on 2023-05-04 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0031_alter_cartproduct_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart', through='onlineStoreApp.CartProduct', to='onlineStoreApp.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(db_column='price', decimal_places=2, default=0, max_digits=10),
        ),
    ]
