# Generated by Django 4.1.7 on 2023-04-20 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0010_productinfo_description_productinfo_gluten_free_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinfo',
            name='organic',
            field=models.BooleanField(db_column='organic', default=False),
        ),
    ]
