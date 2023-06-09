# Generated by Django 4.1.7 on 2023-04-28 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('onlineStoreApp', '0025_remove_cart_retailer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.BigIntegerField(db_column='date', default=1682671364),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.IntegerField(db_column='price', default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user_id',
            field=models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
