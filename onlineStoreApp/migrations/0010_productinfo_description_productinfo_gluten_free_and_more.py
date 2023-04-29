# Generated by Django 4.1.7 on 2023-04-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStoreApp', '0009_subsubcategory_subsubsubcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinfo',
            name='description',
            field=models.TextField(blank=True, db_column='description', null=True),
        ),
        migrations.AddField(
            model_name='productinfo',
            name='gluten_free',
            field=models.BooleanField(db_column='gluten_free', default=False),
        ),
        migrations.AddField(
            model_name='productinfo',
            name='lactose_free',
            field=models.BooleanField(db_column='lactose_free', default=False),
        ),
        migrations.AddField(
            model_name='productinfo',
            name='no_preserv',
            field=models.BooleanField(db_column='no_preserv', default=False),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='component',
            field=models.TextField(blank=True, db_column='component', null=True),
        ),
    ]