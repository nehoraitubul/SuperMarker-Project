# Generated by Django 4.1.7 on 2023-03-29 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('onlineStoreApp', '0002_alter_price_price_alter_product_catalog_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.BigIntegerField(db_column='date')),
                ('price', models.IntegerField(db_column='price')),
                ('cart_status', models.BooleanField(db_column='discount_status', default=True)),
                ('retailer_id', models.ForeignKey(db_column='retailer_id', on_delete=django.db.models.deletion.RESTRICT, to='onlineStoreApp.retailer')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'carts',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(db_column='quantity')),
                ('cart_id', models.ForeignKey(db_column='cart_id', on_delete=django.db.models.deletion.RESTRICT, to='onlineStoreApp.cart')),
                ('product_id', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.RESTRICT, to='onlineStoreApp.product')),
            ],
            options={
                'db_table': 'cart_products',
                'ordering': ['id'],
            },
        ),
    ]
