# Generated by Django 4.1.7 on 2023-04-28 11:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0026_alter_cart_date_alter_cart_price_alter_cart_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_key',
            field=models.UUIDField(db_column='cart_key', default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.BigIntegerField(db_column='date', default=1682680995),
        ),
    ]
