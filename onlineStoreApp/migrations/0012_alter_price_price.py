# Generated by Django 4.1.7 on 2023-04-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0011_productinfo_organic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.DecimalField(db_column='price', decimal_places=2, max_digits=10),
        ),
    ]
